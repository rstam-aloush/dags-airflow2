"""
# tba_wiese
This DAG updates the following datasets:

- [100269](https://data.bs.ch/explore/dataset/100269)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the tba_wiese docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 31),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch", "rstam.aloush@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('tba_wiese', default_args=default_args, schedule_interval="30 * * * *", catchup=False,
         dagrun_timeout=timedelta(minutes=50)) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='tba_wiese:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m tba_wiese.etl',
        container_name='tba_wiese--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
