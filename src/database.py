import os
import psycopg2
import json
from psycopg2.extras import Json

# 환경 변수에서 설정 로드
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "modeldb")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

# 연결 문자열 
conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_connection():
    return psycopg2.connect(conn_string)

def save_job_data(job_id, data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO jobs (job_id, status, data) VALUES (%s, %s, %s)",
                (job_id, "pending", Json(data))
            )

def get_job_data(job_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT data FROM jobs WHERE job_id = %s", (job_id,))
            result = cur.fetchone()
            return result[0] if result else None

def update_job_status(job_id, status):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET status = %s, updated_at = NOW() WHERE job_id = %s",
                (status, job_id)
            )

def get_job_status(job_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT status FROM jobs WHERE job_id = %s", (job_id,))
            result = cur.fetchone()
            return result[0] if result else None

def save_job_result(job_id, result):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET result = %s WHERE job_id = %s",
                (Json(result), job_id)
            )

def get_job_result(job_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT result FROM jobs WHERE job_id = %s", (job_id,))
            result = cur.fetchone()
            return result[0] if result else None

def save_job_error(job_id, error):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET error = %s WHERE job_id = %s",
                (error, job_id)
            )

# 웹훅 관련 함수들
def set_job_webhook(job_id, webhook_url):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET webhook_url = %s WHERE job_id = %s",
                (webhook_url, job_id)
            )

def get_job_webhook(job_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT webhook_url FROM jobs WHERE job_id = %s", (job_id,))
            result = cur.fetchone()
            return result[0] if result else None