FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \

COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]