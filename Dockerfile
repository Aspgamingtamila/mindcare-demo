FROM python:3.12-slim

WORKDIR /app
COPY . .

# Render mounts the persistent SQLite disk at /var/data.
ENV DATABASE_PATH=/var/data/mindcare-demo.db
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
CMD ["python", "server.py"]
