"""
# staka_kandidaturen.py
This DAG helps populating the following datasets:

[100316](https://data.bs.ch/explore/dataset/100316)
[100317](https://data.bs.ch/explore/dataset/100317)
[100333](https://data.bs.ch/explore/dataset/100333)
[100334](https://data.bs.ch/explore/dataset/100334)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the staka_kandidaturen.py docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('staka_kandidaturen', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='staka_kandidaturen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m staka_kandidaturen.etl',
        container_name='staka_kandidaturen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Wahlen-Abstimmungen/Kandidaturen",
                      target="/code/data-processing/staka_kandidaturen/data_orig", type="bind")]
    )
