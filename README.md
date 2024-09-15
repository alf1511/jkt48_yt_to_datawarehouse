# JKT48 YouTube Video Data | ETL with Apache Airflow

![image](https://github.com/user-attachments/assets/f53df9ef-b8e9-4908-ab28-b7a385156f1a)

## Project Description
This project automates the transfer of data from YouTube to a local PostgreSQL data warehouse using Apache Airflow. It involves creating two DAGs (Directed Acyclic Graphs). The first DAG is responsible for extracting and transforming YouTube video data, which is achieved using the YouTube Data API v3 and Python. The second DAG monitors the S3 bucket for the presence of a specific key file. If the file is found, it triggers the S3-to-PostgreSQL loading process. This is accomplished using the S3KeySensor object.

## Features

- Extract YouTube Video Data using YouTube v3 API
- Transform the YouTube Video Comments Data
- Upload the transformed data to AWS S3 Bucket
- Monitor the S3 bucket to Load the data from S3 bucket to PostgreSQL

## Installation

### Prerequisites

- Python
- Docker
- AWS Service

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/username/repository.git](https://github.com/alf1511/jkt48_yt_to_datawarehouse.git
   cd repository
   
2. Build the docker image:

   ```bash
   docker build -t [image name]:[version] .
   
3. Start the containers using docker-compose:

   ```bash
   docker-compose up
   
4. Access the Airflow and PgAdmin UI:

   Access **localhost:8080** for the Airflow UI and **localhost:5050** for the PgAdmin
   > **Note** <br><br> Make sure to modify the `API_KEY` in `jkt48_yt_s3_to_postgresql.py`, besides that make sure to register the required connections (AWS Service and PostgreSQL) through Airflow UI.
   
