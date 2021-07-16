FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . .

RUN apt update && \
    apt install -y build-essential libssl-dev libffi-dev && \
    pip install -r requirements.txt && \
    apt clean

CMD uvicorn app.main:app --host=0.0.0.0 --port=80
