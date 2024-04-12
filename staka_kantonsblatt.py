"""
# staka_kantonsblatt.py
This DAG updates the following datasets:

- [100352](https://data.bs.ch/explore/dataset/100352)
"""

import time
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the staka_kantonsblatt docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 3, 1),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('staka_kantonsblatt', default_args=default_args, schedule_interval='30 0 * * *',
         catchup=False) as dag:
    dag.doc_md = __doc__
    upload_kantonsblatt = DockerOperator(
        task_id='upload_kantonsblatt',
        image='staka_kantonsblatt:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m staka_kantonsblatt.etl',
        container_name='staka_kantonsblatt',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )

    # https://stackoverflow.com/questions/55002234/apache-airflow-delay-a-task-for-some-period-of-time
    # Wait for 30 minutes for data to be updated
    delay_python_task: PythonOperator = PythonOperator(task_id="delay_python_task",
                                                       python_callable=lambda: time.sleep(1800))

    upload_baupublikation = DockerOperator(
        task_id='upload_baupublikation',
        image='staka_baupublikationen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m staka_baupublikationen.etl',
        container_name='staka_baupublikationen',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )

    upload_kantonsblatt >> delay_python_task >> upload_baupublikation
