"""
# stata_parzellen
This DAG updates the following datasets:

- [100202](https://data.bs.ch/explore/dataset/100202)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the stata_parzellen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('stata_parzellen', default_args=default_args, schedule_interval="0 2 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='stata_parzellen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m stata_parzellen.etl',
        container_name='stata_parzellen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Parzellen",
                      target="/code/data-processing/stata_parzellen/data_orig", type="bind")]
    )
