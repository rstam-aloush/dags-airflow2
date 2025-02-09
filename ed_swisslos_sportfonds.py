"""
# ed_swisslos_sportfonds
This DAG updates the following datasets:

- [100221](https://data.bs.ch/explore/dataset/100221)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the ed_swisslos_sportfonds docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('ed_swisslos_sportfonds', default_args=default_args, schedule_interval='0 2 * * *',
         catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='ed_swisslos_sportfonds:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m ed_swisslos_sportfonds.etl',
        container_name='ed_swisslos_sportfonds',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/ED-Swisslos-Sportfonds",
                      target="/code/data-processing/ed_swisslos_sportfonds/data_orig", type="bind")]
    )