# 베이스 이미지 (Python 3.12, 필요하면 slim 버전)
FROM python:3.12-slim

# 작업 디렉터리 설정
WORKDIR /app

# 시스템 의존성 설치 (필요 시)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치 (최신 버전으로 설치)
RUN pip install --no-cache-dir poetry

# poetry.lock, pyproject.toml 먼저 복사 (캐시 활용용)
COPY pyproject.toml poetry.lock* /app/

# 의존성 설치 (가상환경 없이 --no-root)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# 소스코드 전체 복사
COPY src /app/src

# PYTHONPATH 설정 (필요시)
ENV PYTHONPATH=/app/src

# uvicorn 실행 포트 지정 (Cloudtype 같은 곳에서 포트 맞춰야 함)
EXPOSE 8000

# 컨테이너 시작 명령어
CMD ["uvicorn", "autto.main:app", "--host", "0.0.0.0", "--port", "8080"]
