FROM python:3.12-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y curl build-essential && apt-get clean

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -

# Poetry 환경 변수 설정
ENV PATH="/root/.local/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY src ./src

# virtualenv 사용 안 하도록 설정
RUN poetry config virtualenvs.create false

# 의존성 설치
RUN poetry install --no-interaction --no-ansi

# 포트 오픈
EXPOSE 8000

# 실행 명령
CMD ["poetry", "run", "uvicorn", "src.autto.main:app", "--host", "0.0.0.0", "--port", "8000"]
