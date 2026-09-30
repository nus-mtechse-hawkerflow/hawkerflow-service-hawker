FROM python:3.14.7-slim
WORKDIR /usr/local/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ .
COPY target/deployment/resources ./resources
COPY target/deployment/vault ./vault

EXPOSE 8080

RUN useradd app
USER app

CMD ["python3", "main.py"]
