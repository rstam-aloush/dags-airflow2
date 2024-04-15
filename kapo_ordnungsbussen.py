"""
# kapo_ordnungsbussen
This DAG updates the following datasets:

- [100058](https://data.bs.ch/explore/dataset/100058)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the kapo_ordnungsbussen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 26),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('kapo_ordnungsbussen', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='kapo_ordnungsbussen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m kapo_ordnungsbussen.src.etl',
        container_name='kapo_ordnungsbussen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/KaPo/Ordnungsbussen",
                      target="/code/data-processing/kapo_ordnungsbussen/data_orig", type="bind")]
    )
