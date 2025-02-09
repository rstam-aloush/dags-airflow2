"""
# ibs_parkhaus_bewegungen.py
This DAG updates the following datasets:

- [100198](https://data.bs.ch/explore/dataset/100198)

"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the ibs_parkhaus_bewegungen.py docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('ibs_parkhaus_bewegungen', default_args=default_args, schedule_interval='0 1 * * *', catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='ibs_parkhaus_bewegungen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m ibs_parkhaus_bewegungen.etl',
        container_name='ibs_parkhaus_bewegungen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/ibs-parkhaeuser/Ein-Ausfahrten",
                      target="/code/data-processing/ibs_parkhaus_bewegungen/data_orig", type="bind")]
    )
