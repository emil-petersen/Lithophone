FROM python:3.6-alpine

WORKDIR /usr/src/app
COPY src .
RUN pip install --no-cache-dir gunicorn

ENV WORKERS=4

EXPOSE 8000

USER nobody

CMD gunicorn --bind 0.0.0.0:8000 -w $WORKERS lithophone:app
