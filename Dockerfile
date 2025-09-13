from python:3.6

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


CMD ["python", "demo"]
