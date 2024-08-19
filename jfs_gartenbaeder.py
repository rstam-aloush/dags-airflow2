"""
# jfs_gartenbaeder
This DAG updates the following datasets:

- [100384](https://data.bs.ch/explore/dataset/100384)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'rstam.aloush',
    'description': 'Run the jfs_gartenbaeder docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 8, 14),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('jfs_gartenbaeder', default_args=default_args, schedule_interval="*/15 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='jfs_gartenbaeder:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m jfs_gartenbaeder.etl',
        container_name='jfs_gartenbaeder',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )