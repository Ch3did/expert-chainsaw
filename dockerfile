FROM python:3.12-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

RUN chmod +x /app/entrypoint.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]