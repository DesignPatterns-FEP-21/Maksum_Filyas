#Він, по суті, є інструкцією для збірки Docker-образу: він бере чистий Python, 
#встановлює всі потрібні бібліотеки (з requirements.txt), 
#копіює всередину код вашого проєкту (app та frontend) і вказує, 
#яку команду (uvicorn) запустити, щоб ваш додаток запрацював

# Використовуємо офіційний Python образ
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл залежностей
COPY ./requirements.txt /app/requirements.txt

# Встановлюємо залежності
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіюємо код програми
COPY ./app /app/app
COPY ./frontend /app/frontend

# Вказуємо порт, який слухає FastAPI
EXPOSE 8000

# Запускаємо Uvicorn сервер
# main:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]