"""
# bafu_hydro_daten
This DAG updates the following datasets:

- [100089](https://data.bs.ch/explore/dataset/100089)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the bafu_hydrodaten docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 22),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('bafu_hydro_daten', default_args=default_args, schedule_interval="*/5 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='bafu_hydrodaten:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m bafu_hydrodaten.etl_https',
        container_name='bafu_hydrodaten',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[{
            "Source": "/data/dev/workspace/data-processing",
            "Target": "/code/data-processing",
            "Type": "bind",
            "ReadOnly": False
        }]
    )
