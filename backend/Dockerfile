FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY vision_app ./vision_app

EXPOSE 8000

CMD ["uvicorn", "vision_app.api:app", "--host", "0.0.0.0", "--port", "8000"]
