"""
# parlamentsdienst_gr_abstimmungen
This DAG updates the following datasets:

- [100186](https://data.bs.ch/explore/dataset/100186)
- [100188](https://data.bs.ch/explore/dataset/100188)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the parlamentsdienst_gr_abstimmungen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 12),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch",
              "nicolas.maire@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('parlamentsdienst_gr_abstimmungen', default_args=default_args, schedule_interval="*/2 * * * *",
         catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='parlamentsdienst_gr_abstimmungen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m parlamentsdienst_gr_abstimmungen.etl',
        container_name='parlamentsdienst_gr_abstimmungen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
