FROM python:3.11-slim

WORKDIR /app
ENV ENV=production
ENV PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY .env.production /app/.env.production

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
