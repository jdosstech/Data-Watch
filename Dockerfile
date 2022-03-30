FROM python:3.8.9

ENV SRC_DIR /app

COPY backend/* ${SRC_DIR}/

WORKDIR ${SRC_DIR}

RUN python3  -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade pyOpenSSL && \
    python3  -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000:8000

CMD ["python3", "monitor.py"]
