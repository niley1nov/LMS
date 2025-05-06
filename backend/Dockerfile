FROM python:3.11-slim

WORKDIR /app
ENV ENV=production
ENV PORT=8080          # default; Cloud Run will override this

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY .env.production /app/.env.production

# use shell form so $PORT is substituted
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
