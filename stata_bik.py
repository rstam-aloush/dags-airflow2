"""
# stata_bik
This DAG updates the following datasets:

- [100003](https://data.bs.ch/explore/dataset/100003)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the stata_bik docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 3, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('stata_bik', default_args=default_args, schedule_interval="0 10 * * *",
         catchup=False) as dag:
    dag.doc_md = __doc__

    ods_publish = DockerOperator(
        task_id='stata_bik',
        image='stata_bik:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m stata_bik.etl',
        container_name='stata_bik',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/BIK",
                      target="/code/data-processing/stata_bik/data_orig", type="bind")],
    )
