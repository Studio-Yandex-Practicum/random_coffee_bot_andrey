FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["bash", "-c", "python django_app.py runserver 0:8000 & python bot.py"]