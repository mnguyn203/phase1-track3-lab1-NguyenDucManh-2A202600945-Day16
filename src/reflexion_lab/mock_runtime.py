from __future__ import annotations
import os
import time
from typing import Tuple
from pydantic import BaseModel
import openai

from .schemas import QAExample, JudgeResult, ReflectionEntry
from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM
from .utils import normalize_answer

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_client = None
def get_client() -> openai.Client:
    global _client
    if _client is None:
        _client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_DELAY = float(os.getenv("API_DELAY", "0.5"))

FAILURE_MODE_BY_QID = {
    "hp2": "incomplete_multi_hop",
    "hp4": "wrong_final_answer",
    "hp6": "entity_drift",
    "hp8": "entity_drift"
}

def format_context(context_chunks) -> str:
    return "\n\n".join([f"[{i+1}] {chunk.title}\n{chunk.text}" for i, chunk in enumerate(context_chunks)])

def actor_answer(example: QAExample, attempt_id: int, agent_type: str, reflection_memory: list[str]) -> Tuple[str, int, float]:
    prompt = f"Question: {example.question}\n\nContext:\n{format_context(example.context)}\n\n"
    if reflection_memory:
        prompt += f"Reflection Memory (Lessons from past attempts):\n" + "\n---\n".join(reflection_memory) + "\n\n"
    prompt += "Answer concisely:"
    
    start_time = time.time()
    try:
        response = get_client().chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": ACTOR_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        answer = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens if response.usage else 0
    except Exception as e:
        print(f"Actor Error: {e}")
        answer = "Error generating answer"
        tokens = 0
    latency = (time.time() - start_time) * 1000
    if API_DELAY > 0:
        time.sleep(API_DELAY)
    return answer, tokens, latency

def evaluator(example: QAExample, answer: str) -> Tuple[JudgeResult, int, float]:
    prompt = f"Question: {example.question}\nGold Answer: {example.gold_answer}\nPredicted Answer: {answer}\n\nEvaluate the predicted answer."
    
    start_time = time.time()
    try:
        response = get_client().beta.chat.completions.parse(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": EVALUATOR_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            response_format=JudgeResult
        )
        judge = response.choices[0].message.parsed
        tokens = response.usage.total_tokens if response.usage else 0
    except Exception as e:
        print(f"Evaluator Error: {e}")
        is_correct = normalize_answer(example.gold_answer) == normalize_answer(answer)
        judge = JudgeResult(score=1 if is_correct else 0, reason="Fallback due to API error")
        tokens = 0
    latency = (time.time() - start_time) * 1000
    if API_DELAY > 0:
        time.sleep(API_DELAY)
    return judge, tokens, latency

def reflector(example: QAExample, attempt_id: int, judge: JudgeResult) -> Tuple[ReflectionEntry, int, float]:
    prompt = f"Question: {example.question}\n\nIncorrect Predicted Answer: (Failed attempt)\n\nEvaluator Reason: {judge.reason}\n\nAnalyze the failure."
    
    start_time = time.time()
    try:
        response = get_client().beta.chat.completions.parse(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": REFLECTOR_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            response_format=ReflectionEntry
        )
        reflection = response.choices[0].message.parsed
        reflection.attempt_id = attempt_id
        tokens = response.usage.total_tokens if response.usage else 0
    except Exception as e:
        print(f"Reflector Error: {e}")
        reflection = ReflectionEntry(attempt_id=attempt_id, failure_reason="API error", lesson="N/A", next_strategy="Try again")
        tokens = 0
    latency = (time.time() - start_time) * 1000
    if API_DELAY > 0:
        time.sleep(API_DELAY)
    return reflection, tokens, latency
