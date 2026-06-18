# ប្រើប្រាស់ Python ជំនាន់ស្រាល
FROM python:3.10-slim

# ដំឡើងកម្មវិធី FFmpeg សម្រាប់កាត់តសំឡេង
RUN apt-get update && apt-get install -y ffmpeg

# កំណត់ទីតាំងធ្វើការក្នុង Server
WORKDIR /app

# ចម្លងកូដទាំងអស់របស់យើងចូលទៅក្នុង Server
COPY . /app

# ដំឡើង Library ដែលមានក្នុង requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# បញ្ឆេះ Telegram Bot ឲ្យដើរពីក្រោយ រួចបញ្ឆេះ API ឲ្យវេបសាយដើរពីមុខ
CMD python backend/bot.py & uvicorn backend.api:app --host 0.0.0.0 --port $PORT