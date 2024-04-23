FROM python:3.12

RUN mkdir /tp_app_fastapi

WORKDIR /tp_app_fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /tp_app_fastapi/docker/*.sh

CMD [ "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]