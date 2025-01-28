"""
# bafu_hydro_daten
This DAG updates the following datasets:

- [100271](https://data.bs.ch/explore/dataset/100271)
- [100272](https://data.bs.ch/explore/dataset/100272)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the bafu_hydrodaten_vorhersagen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 22),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('bafu_hydrodaten_vorhersagen', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='bafu_hydrodaten_vorhersagen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m bafu_hydrodaten_vorhersagen.etl',
        container_name='bafu_hydrodaten_vorhersagen',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
