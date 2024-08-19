"""
# staka_staatskalender.py
This DAG updates the following repositories:

[Starter Code on GitHub](https://github.com/opendatabs/startercode-opendatabs)
[Starter Code on Renku](https://renkulab.io/projects/opendatabs/startercode-opendatabs)

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
    'description': 'Run the startercode-generator-bs docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 7, 3),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch", "rstam.aloush@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('startercode-generator-bs', default_args=default_args, schedule_interval='0 8/12 * * *',
         catchup=False) as dag:
    dag.doc_md = __doc__
    update = DockerOperator(
        task_id='update',
        image='startercode-generator-bs:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m updater',
        container_name='startercode-generator-bs',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/startercode-generator-bs", target="/code/startercode-generator-bs", type="bind")]
    )

    update_github = DockerOperator(
        task_id='update_github',
        image='update_github:latest',
        api_version='auto',
        auto_remove='force',
        environment={'https_proxy': https_proxy},
        command='/bin/bash /code/startercode-generator-bs/update_github.sh ',
        container_name='update_github',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/startercode-generator-bs", target="/code/startercode-generator-bs", type="bind")]
    )

    update >> update_github
