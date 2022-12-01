FROM python:3.8-alpine

RUN apk update \
  && apk add --update --no-cache git openssh-client \
  && addgroup -S -g 1001 anime \
  && adduser -S -D -h /home/anime -u 1001 -G anime anime

WORKDIR /app

COPY --chown=root:root src/ .
RUN pip3 install -r requirements.txt && pip3 install gunicorn

USER anime
EXPOSE 8000
CMD ["gunicorn", "--threads", "8", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
