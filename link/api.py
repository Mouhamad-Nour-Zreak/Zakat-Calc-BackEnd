# api.py
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from link.state import state_manager

api = FastAPI()

class Answer(BaseModel):
    answer: str

@api.get("/start")
async def start_engine():
    try:
        await run_in_threadpool(state_manager.start_engine)
        result = await run_in_threadpool(state_manager.get_question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.post("/submit-answer")
async def submit_answer(answer: Answer):
    try:
        result = await run_in_threadpool(state_manager.provide_answer, answer.answer)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
