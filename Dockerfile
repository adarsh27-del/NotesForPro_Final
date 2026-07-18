FROM python:3.10-slim

RUN apt-get update && apt-get install -y graphviz

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/usr/bin:${PATH}"

CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT