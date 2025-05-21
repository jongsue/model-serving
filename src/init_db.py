import os
import psycopg2
import time

# 환경 변수에서 설정 로드
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "modeldb")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

# 연결 문자열
conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def wait_for_db(max_attempts=60, interval=5):
    """데이터베이스가 준비될 때까지 대기"""
    attempts = 0
    while attempts < max_attempts:
        try:
            conn = psycopg2.connect(conn_string)
            conn.close()
            print("데이터베이스 연결 성공!")
            return True
        except Exception as e:
            print(f"데이터베이스 연결 시도 중 ({attempts+1}/{max_attempts}): {str(e)}")
            attempts += 1
            time.sleep(interval)
    
    return False

def init_database():
    """필요한 테이블 생성"""
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    
    # jobs 테이블 생성
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id VARCHAR(36) PRIMARY KEY,
        status VARCHAR(20) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
        data JSONB,
        result JSONB,
        error TEXT,
        webhook_url TEXT
    );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("테이블 생성 완료!")

if __name__ == "__main__":
    if wait_for_db():
        init_database()
    else:
        print("데이터베이스 연결 시간 초과!")
        exit(1)