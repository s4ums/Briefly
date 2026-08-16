FROM python:3.12-slim

WORKDIR /app

# Kept minimal for now. Later milestones (e.g. Milestone 13 diarization,
# Milestone 11 PDF export) may require additional system packages such as
# ffmpeg or libpq-dev — add them there, not here.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
