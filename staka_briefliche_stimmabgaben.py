"""
# staka_briefliche_stimmabgaben_1.py
This DAG helps populating the following datasets:

- [100223](https://data.bs.ch/explore/dataset/100223)
- [100224](https://data.bs.ch/explore/dataset/100224)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'hester.pieters',
    'description': 'Run the staka_briefliche_stimmabgaben.py docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('staka_briefliche_stimmabgaben_3', default_args=default_args, schedule_interval='30 * * * *',
         catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='staka_briefliche_stimmabgaben:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m staka_briefliche_stimmabgaben.etl',
        container_name='staka_briefliche_stimmabgaben--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/staka-abstimmungen",
                      target="/code/data-processing/staka_briefliche_stimmabgaben/data", type="bind")]
    )
