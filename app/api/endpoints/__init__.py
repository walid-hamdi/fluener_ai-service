"""Combine all endpoints"""
from fastapi import APIRouter
from app.api.endpoints import stt, tts, llm, health

router = APIRouter()

router.include_router(stt.router)
router.include_router(tts.router)
router.include_router(llm.router)
router.include_router(health.router)