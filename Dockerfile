FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y netcat

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

RUN groupadd -r app \
    && useradd -d /app -r -g app app

USER app

COPY --chown=app:app . .

EXPOSE 8000

CMD [ "bash", "./src/app/run.sh"]
