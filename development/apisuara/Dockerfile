# Menggunakan image dasar Python resmi.
FROM python:3.10-slim

# Menetapkan direktori kerja di dalam container.
WORKDIR /app

# Menyalin file requirements.txt dan menginstal dependensi.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Menyalin seluruh direktori saat ini ke dalam container.
COPY . .

# Menetapkan perintah untuk menjalankan aplikasi Flask.

