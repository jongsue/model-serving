import os
from celery import Celery
import numpy as np
import torch
import database
import requests
from model import YourModel

# 환경 변수에서 설정 로드
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

# Celery 앱 설정
app = Celery('model_tasks',
             broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
             backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/1')

# 모델 로드
model = YourModel()
model.eval()

@app.task
def process_model_task(job_id):
    try:
        # 작업 상태 업데이트
        database.update_job_status(job_id, "processing")
        
        # 데이터 로드
        data = database.get_job_data(job_id)
        
        # 모델 실행 (1-3분 소요)
        input_data = np.array(data, dtype=np.float32)
        input_tensor = torch.tensor(input_data)
        
        with torch.no_grad():
            output = model(input_tensor).numpy().tolist()
        
        # 결과 저장
        database.save_job_result(job_id, output)
        database.update_job_status(job_id, "completed")
        
        # 웹훅 호출 (선택 사항)
        webhook_url = database.get_job_webhook(job_id)
        if webhook_url:
            requests.post(webhook_url, json={"job_id": job_id, "status": "completed"})
            
        return True
    
    except Exception as e:
        database.update_job_status(job_id, "failed")
        database.save_job_error(job_id, str(e))
        return False