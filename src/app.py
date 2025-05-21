import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import uuid
from celery_worker import process_model_task
import database

app = FastAPI()

class PredictionRequest(BaseModel):
    data: list  # 8000x100 데이터

class JobResponse(BaseModel):
    job_id: str
    status: str

class ResultResponse(BaseModel):
    result: list
    status: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=JobResponse)
async def predict(request: PredictionRequest):
    # 작업 ID 생성
    job_id = str(uuid.uuid4())
    
    # 데이터 저장
    database.save_job_data(job_id, request.data)
    
    # Celery 작업 시작 (비동기)
    process_model_task.delay(job_id)
    
    return JobResponse(job_id=job_id, status="processing")

@app.get("/status/{job_id}", response_model=JobResponse)
async def get_status(job_id: str):
    status = database.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse(job_id=job_id, status=status)

@app.get("/result/{job_id}", response_model=ResultResponse)
async def get_result(job_id: str):
    status = database.get_job_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if status != "completed":
        return ResultResponse(result=[], status=status)
    
    result = database.get_job_result(job_id)
    return ResultResponse(result=result, status=status)

# 웹훅 설정 엔드포인트
@app.post("/webhook-config/{job_id}")
async def set_webhook(job_id: str, webhook_url: str):
    database.set_job_webhook(job_id, webhook_url)
    return {"status": "webhook configured"}