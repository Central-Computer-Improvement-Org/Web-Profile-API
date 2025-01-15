FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    python3-dev \
    postgresql-client  \
    postgresql-server \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python3 manage.py migrate

EXPOSE 8181

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]