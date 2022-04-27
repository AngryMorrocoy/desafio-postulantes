FROM python:3.10-alpine3.15
WORKDIR /app/

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont

ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=0

RUN addgroup -S pptruser && adduser -S -G pptruser pptruser \
    && mkdir -p /home/pptruser/Downloads /app \
    && chown -R pptruser:pptruser /home/pptruser \
    && chown -R pptruser:pptruser /app

USER pptruser

ENV PATH=${PATH}:/home/pptruser/.local/bin

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD hypercorn app:app --bind 0.0.0.0:$PORT
