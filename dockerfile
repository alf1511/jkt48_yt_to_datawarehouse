FROM apache/airflow:latest

USER root

RUN apt-get update && \
    apt-get install -y && \
    apt-get clean

USER airflow

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
