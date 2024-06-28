FROM python:3.12.0-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=propysolver.settings

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]