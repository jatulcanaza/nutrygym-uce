FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO, incluido main.py
COPY . .

EXPOSE 3003

# Cambiar de app.main a main
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3003"]