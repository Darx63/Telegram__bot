FROM python:3.8

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get install -y vim nano 

WORKDIR /app

COPY bot.py bot.py

entrypoint ["python3","bot.py"]