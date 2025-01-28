"""
# stata_daily_upload
This DAG updates datasets referenced in https://github.com/opendatabs/data-processing/blob/master/stata_daily_upload/etl.py:
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the stata_daily_upload docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=30)
}

with DAG('stata_daily_upload', default_args=default_args, schedule_interval="*/15 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='stata_daily_upload:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m stata_daily_upload.etl',
        container_name='stata_daily_upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch", target="/code/data-processing/stata_daily_upload/data", type="bind")]
    )
