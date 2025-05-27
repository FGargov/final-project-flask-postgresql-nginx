FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ .
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] # for production