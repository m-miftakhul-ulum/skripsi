# Menggunakan image dasar Python resmi.
FROM python:3.10-slim

# Set environment variable
# ENV PYTHONUNBUFFERED=1

# Buat direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt ke dalam direktori kerja
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari direktori lokal ke dalam direktori kerja di container
COPY . /app/

# Expose port yang akan digunakan oleh aplikasi
EXPOSE 5001

# Perintah untuk menjalankan aplikasi
CMD ["python", "dekripsi.py"]

