"""
# ed_schulferien
This DAG updates the following dataset:

- [100397](https://data.bs.ch/explore/dataset/100397)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'renato.farruggio',
    'description': 'Run the ed_schulferien docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 9, 18),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('ed_schulferien', default_args=default_args, schedule_interval="0 0 1 * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='ed_schulferien:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m ed_schulferien.etl',
        container_name='ed_schulferien--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
