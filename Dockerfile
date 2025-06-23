# Dockerfile (Autto-Server/Dockerfile)
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --upgrade pip && pip install poetry

# pyproject.toml, poetry.lock 복사
COPY pyproject.toml poetry.lock ./

# src 폴더 복사
COPY src/ ./src/

# README.md 복사 (필수, 설치 에러 방지)
COPY README.md ./

# poetry 환경 설정 및 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-ansi

# 포트 설정
EXPOSE 8000

# 앱 실행
CMD ["poetry", "run", "uvicorn", "src.autto.main:app", "--host", "0.0.0.0", "--port", "8000"]
