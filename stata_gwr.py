"""
# stata_gwr
This DAG updates the following datasets:

- [100230](https://data.bs.ch/explore/dataset/100230)
- [100231](https://data.bs.ch/explore/dataset/100231)
- [100232](https://data.bs.ch/explore/dataset/100232)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the stata_gwr docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch", "rstam.aloush@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('stata_gwr', default_args=default_args, schedule_interval="25 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='stata_gwr:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m stata_gwr.etl',
        container_name='stata_gwr--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
