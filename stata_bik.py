"""
# ods_publish
This DAG updates the following datasets:

- [100003](https://data.bs.ch/explore/dataset/100003)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the ods_publish docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 3, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('ods_publish', default_args=default_args, schedule_interval="0 5 * * *",
         catchup=False) as dag:
    dag.doc_md = __doc__

    ods_publish = DockerOperator(
        task_id='ods-publish',
        image='ods-publish:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m ods_publish.etl_id 100003',
        container_name='ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")],
    )
