"""
# aue_rues
This DAG updates the following datasets:

- [100046](https://data.bs.ch/explore/dataset/100046)
- [100323](https://data.bs.ch/explore/dataset/100323)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the aue_rues docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 19),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch", "rstam.aloush@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('aue_rues', default_args=default_args, schedule_interval="*/10 * * * *", catchup=False,
         dagrun_timeout=timedelta(minutes=8)) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='aue_rues:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m aue_rues.etl',
        container_name='aue_rues--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
