# 1. Python imajı
FROM python:3.11-slim

# 2. Çalışma dizini oluştur
WORKDIR /app


# Sistem bağımlılıkları (ffmpeg dahil)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# 3. Gereken dosyaları kopyala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Proje dosyalarını kopyala
COPY . .

# 5. Output klasörü oluştur
RUN mkdir -p output

# 6. Uvicorn ile başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

