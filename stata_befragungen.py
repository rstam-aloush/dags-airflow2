"""
# stata_befragungen
This DAG updates the datasets outlined [here](https://data.bs.ch/explore/?sort=modified&q=befragung+statistisches+amt).
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the stata_befragungen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch",
              "nicolas.maire@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('stata_befragungen', default_args=default_args, schedule_interval="5,35 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='stata_befragungen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m stata_befragungen.src.etl',
        container_name='stata_befragungen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Befragungen/55plus_Ablage_StatA",
                      target="/code/data-processing/stata_befragungen/data_orig/55plus", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Befragungen/55plus_OGD",
                      target="/code/data-processing/stata_befragungen/data/55plus", type="bind")
                ]
    )
