FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn openai pydantic

CMD ["uvicorn", "env:app", "--host", "0.0.0.0", "--port", "7860"]
