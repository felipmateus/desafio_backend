FROM python:3.10.6

RUN apt-get update && \
    apt-get install -y python3-pip python-dev


WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt


EXPOSE 3001

CMD ["python3", "app.py"]