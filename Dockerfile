FROM python:3.11-slim

WORKDIR /app

COPY . /app   

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

ENV PYTHONPATH="/app/orchestration:/app"

CMD ["uvicorn", "orchestration.main:app", "--host", "0.0.0.0", "--port", "8000"]
