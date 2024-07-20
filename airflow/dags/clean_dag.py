from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from scripts.download_transactions import download_data
from scripts.clean import clean

default_args = {
    'owner': 'Ali',
    'email': ['alifadl30@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='ETL',
    default_args=default_args,
    schedule_interval='@weekly',  # run every week
    start_date=days_ago(0),
    catchup=False,
) as dag:

    download_transactions = PythonOperator(
        task_id='Download Transactions',
        python_callable=download_data
    )

    clean_transactions = PythonOperator(
        task_id='Clean_Transactions',
        python_callable=clean
    )

    download_transactions >> clean_transactions
