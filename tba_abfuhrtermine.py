"""
# tba_abfuhrtermine
This DAG updates the following datasets:

- [100096](https://data.bs.ch/explore/dataset/100096)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the tba_abfuhrtermine docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch", "rstam.aloush@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('tba_abfuhrtermine', default_args=default_args, schedule_interval="0 10 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='tba_abfuhrtermine:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m tba_abfuhrtermine.etl',
        container_name='tba_abfuhrtermine',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/mnt/OGD-GVA", target="/code/data-processing/tba_abfuhrtermine/data_orig", type="bind"),
                Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )