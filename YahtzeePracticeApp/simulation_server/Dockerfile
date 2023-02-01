FROM python:3.9-slim-buster

RUN mkdir app

COPY . /app

WORKDIR app

RUN pip install -r requirements.txt && rm requirements.txt

CMD ["python", "server.py"]
