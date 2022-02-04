from python:3.7.12-slim-buster


RUN pip install aiohttp aiodns cchardet prometheus_async prometheus-client

EXPOSE 8000 8000

COPY . /app

ENTRYPOINT ["python"]
