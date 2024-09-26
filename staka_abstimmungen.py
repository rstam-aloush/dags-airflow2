"""
# staka_abstimmungen
This DAG updates the test and live version of the 2 datasets that cover the latest polls:

- [100141](https://data.bs.ch/explore/dataset/100141)
- [100142](https://data.bs.ch/explore/dataset/100142)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the staka_abstimmungen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 29),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch",
              "nicolas.maire@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('staka_abstimmungen', default_args=default_args, schedule_interval="*/2 9-19 * * 7", catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='staka_abstimmungen:latest',
        api_version='auto',
        auto_remove='force',
        command='/bin/bash /code/data-processing/staka_abstimmungen/etl_auto.sh ',
        container_name='staka_abstimmungen',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Wahlen-Abstimmungen",
                      target="/code/data-processing/staka_abstimmungen/data", type="bind")]
    )
