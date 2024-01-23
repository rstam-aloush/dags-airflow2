"""
# kapo_smileys
This DAG updates the following datasets:

- [100268](https://data.bs.ch/explore/dataset/100268)
- [100277](https://data.bs.ch/explore/dataset/100277)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the kapo_smileys docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 22),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('kapo_smileys', default_args=default_args, schedule_interval="15 3 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='kapo_smileys:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m kapo_smileys.etl',
        container_name='kapo_smileys--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/kapo-smileys", target="/code/data-processing/kapo_smileys/data_orig",
                      type="bind")]
    )
