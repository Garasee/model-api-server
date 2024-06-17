FROM python:3.10-slim AS builder

WORKDIR /app

ARG GOOGLE_CREDENTIALS
RUN echo ${GOOGLE_CREDENTIALS} > sa.json

FROM python:3.10-slim

WORKDIR /app

RUN mkdir /app/tmp

COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/sa.json /app/sa.json

EXPOSE 5000

CMD ["python", "app.py"]
