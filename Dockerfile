FROM python:3.7.4-alpine
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app
RUN chmod +x ./gunicorn.sh
ENTRYPOINT ["./gunicorn.sh"]