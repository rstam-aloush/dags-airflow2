"""
# stata_pull_changes
This DAG pulls recent changes from the main/master branch of the following repositories:

- [data-processing](https://github.com/opendatabs/data-processing)
- [dags-airflow2](https://github.com/opendatabs/dags-airflow2)
- [startercode-opendatabs](https://github.com/opendatabs/startercode-generator-bs)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from airflow.models import Variable

# This is set in the Airflow UI under Admin -> Variables
https_proxy = Variable.get("https_proxy")

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run git pull on multiple repositories',
    'depend_on_past': False,
    'start_date': datetime(2024, 4, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch",
              "nicolas.maire@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('stata_pull_changes', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    git_pull = DockerOperator(
        task_id='git_pull',
        image='stata_pull_changes:latest',
        api_version='auto',
        auto_remove='force',
        environment={'https_proxy': https_proxy},
        command='/bin/bash /code/data-processing/stata_pull_changes/pull_changes.sh ',
        container_name='stata_pull_changes',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace", target="/code", type="bind")]
    )
