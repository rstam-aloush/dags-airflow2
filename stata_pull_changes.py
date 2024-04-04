"""
# stata_pull_changes
This DAG pulls recent changes from the main/master branch of the following repositories:

- [data-processing](https://github.com/opendatabs/data-processing)
- [dags-airflow2](https://github.com/opendatabs/dags-airflow2)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run git pull on multiple repositories',
    'depend_on_past': False,
    'start_date': datetime(2024, 4, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('stata_pull_changes', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='stata_pull_changes:latest',
        api_version='auto',
        auto_remove='force',
        command='/bin/bash stata_pull_changes.pull_changes.sh',
        container_name='stata_pull_changes--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace", target="/code", type="bind")]
    )