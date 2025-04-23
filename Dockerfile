# Usa una imagen base con Python
FROM python:3.11-slim

# Evita prompts en la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema para Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip fonts-liberation \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libgtk-3-0 libasound2 xvfb \
    && apt-get clean

# Crea directorio de trabajo
WORKDIR /app

# Copia archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Instala los navegadores de Playwright
RUN python -m playwright install --with-deps

# Expone el puerto para Flask (Railway detecta esto)
EXPOSE 8080

# Ejecuta la app
CMD ["python", "server.py"]
