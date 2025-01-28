"""
# mkb_sammlung_europa.py
This DAG updates the following datasets:

- [100148](https://data.bs.ch/explore/dataset/100148)

"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'hester.pieters',
    'description': 'Run the mkb_sammlung_europa.py docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('mkb_sammlung_europa', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='mkb_sammlung_europa:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m mkb_sammlung_europa.etl',
        container_name='mkb_sammlung_europa--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/PD-Kultur-MKB",
                      target="/code/data-processing/mkb_sammlung_europa/data", type="bind")]
    )
