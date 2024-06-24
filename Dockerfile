# Dockerfile
FROM python:3.10-alpine

ENV TRANSCENDENCE_DIR=/ft_transcendence
ENV TRANSCENDENCE_PROTOCOL=https
ENV POSTGRES_PORT=5432
ENV POSTGRES_HOST=postgres-transcendence
ENV DJANGO_SETTINGS_MODULE=core.settings

COPY requirements.txt $TRANSCENDENCE_DIR/

RUN pip install --no-cache-dir --no-compile -q -r $TRANSCENDENCE_DIR/requirements.txt

RUN mkdir -p $TRANSCENDENCE_DIR; apk add --no-cache openssl

WORKDIR $TRANSCENDENCE_DIR

COPY . $TRANSCENDENCE_DIR

RUN openssl req -newkey rsa:2048 -nodes -keyout /etc/ssl/private/key.pem -x509 -days 365 -out /etc/ssl/certs/cert.pem -subj "/C=BR/ST=SP/L=SãoPaulo/O=42sp/CN=pong.42"

EXPOSE 443

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]