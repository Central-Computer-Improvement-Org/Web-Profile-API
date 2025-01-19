FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    python3-dev \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
COPY entrypoint.sh /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i 's/\r$//g'  /app/entrypoint.sh
RUN chmod +x  /app/entrypoint.sh
RUN mkdir /app/static
RUN mkdir /app/media

COPY . /app/

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/app/entrypoint.sh"]