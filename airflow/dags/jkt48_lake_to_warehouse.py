from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_sql import S3ToSqlOperator  # Import the S3ToSqlOperator
import csv

sql_cols = ['video_id', 'video_title', 'author', 'text', 'published_at', 'like_count']

# Define the CSV parsing function
def parse_csv_to_list(filepath):
    with open(filepath, newline="") as file:
        return list(csv.reader(file))

# Define the DAG
dag = DAG(
    'jkt48_lake_to_warehouse',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False
)

# Wait for the file in S3
wait_for_file = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='commit-bucket',
    bucket_key='jkt48_yt.csv',
    aws_conn_id='aws_s3_conn',
    poke_interval=10,
    mode="poke",
    deferrable=True,
    timeout=60 * 60 * 5,
    soft_fail=True,
    dag=dag
)

# Task to transfer data from S3 to PostgreSQL
transfer_s3_to_sql = S3ToSqlOperator(
    aws_conn_id='aws_s3_conn',
    task_id="transfer_s3_to_sql",
    s3_bucket='commit-bucket',
    s3_key='jkt48_yt.csv',
    table='jkt48_yt_data',  # Table in PostgreSQL
    column_list=sql_cols,  # List of columns in the PostgreSQL table
    parser=parse_csv_to_list,
    sql_conn_id='postgres_conn',  # Connection ID for PostgreSQL
    dag=dag
)

# Set the task dependencies
wait_for_file >> transfer_s3_to_sql
