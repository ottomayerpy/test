FROM python:latest

WORKDIR /anothertest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1 \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_EMAIL=admin@admin.ru

COPY . .

RUN pip install -r requirements.txt
