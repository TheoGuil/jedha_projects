FROM python:3.10

WORKDIR /home/app

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn app:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker