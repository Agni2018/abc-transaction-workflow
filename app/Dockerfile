FROM python:3.12-slim

WORKDIR /app

COPY processor.py .

RUN pip install --no-cache-dir boto3

CMD ["python", "processor.py"]
