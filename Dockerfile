FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

EXPOSE 8765
CMD ["python", "hermeserenao.py", "serve", "--host", "0.0.0.0", "--port", "8765"]
