"""
# tba_sprayereien
This DAG updates the following datasets:

- [......](https://data.bs.ch/explore/dataset/......)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'rstam.aloush',
    'description': 'Run the tba_sprayereien docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 8, 19),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch", "rstam.aloush@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('tba_sprayereien', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='tba_sprayereien:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m tba_sprayereien.etl',
        container_name='tba_sprayereien',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
