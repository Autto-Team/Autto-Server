# 베이스 이미지 설정
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치 (캐싱 전략 포함)
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# pyproject.toml과 poetry.lock 복사
COPY pyproject.toml poetry.lock* ./

# src 코드 복사
COPY src ./src

# Poetry 설치
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# 포트 열기
EXPOSE 8000

# 실행 명령
CMD ["poetry", "run", "uvicorn", "src.autto.main:app", "--host", "0.0.0.0", "--port", "8000"]
