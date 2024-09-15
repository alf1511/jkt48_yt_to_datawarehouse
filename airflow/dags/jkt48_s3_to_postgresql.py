from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator


from plugins.retrieve_youtube import *

API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
PLAYLIST_ID = 'PLqQ7E8cz91tCcfNfAH83nBc8QiFS5vA_O'

def save_comments_to_csv(**kwargs):
    ti = kwargs['ti']
    comments = ti.xcom_pull(task_ids='extract_transform_ytAPI')

    df = pd.DataFrame(comments)
    df.to_csv('/tmp/jkt48_yt.csv', index=False, encoding='utf-8-sig')

    print(f"Comments saved to /tmp/jkt48_yt.csv")

dag = DAG(
    'jkt48_s3_to_postgresql',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 22 * * *',
    catchup=False
)

et_task = PythonOperator(
    task_id='extract_transform_ytAPI',
    python_callable=extract_transform_data,
    op_args = [PLAYLIST_ID, API_KEY],
    dag=dag
)

prepare_data_task = PythonOperator(
    task_id='prepare_data',
    python_callable=save_comments_to_csv,
    provide_context=True,
    dag=dag
)

upload_to_s3_task = LocalFilesystemToS3Operator(
    task_id="upload_to_s3",
    filename='/tmp/jkt48_yt.csv',
    dest_key='jkt48_yt.csv',
    dest_bucket='commit-bucket',
    replace=True,
    aws_conn_id ='aws_s3_conn'
)

et_task >> prepare_data_task >> upload_to_s3_task