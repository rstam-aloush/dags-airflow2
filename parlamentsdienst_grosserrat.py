"""
# parlamentsdienst_grosserrat.py
This DAG updates the following datasets:

- [100307](https://data.bs.ch/explore/dataset/100307)
- [100308](https://data.bs.ch/explore/dataset/100308)
- [100309](https://data.bs.ch/explore/dataset/100309)
- [100310](https://data.bs.ch/explore/dataset/100310)
- [100311](https://data.bs.ch/explore/dataset/100311)
- [100312](https://data.bs.ch/explore/dataset/100312)
- [100313](https://data.bs.ch/explore/dataset/100313)
- [100314](https://data.bs.ch/explore/dataset/100314)
- [100347](https://data.bs.ch/explore/dataset/100347)
- [100348](https://data.bs.ch/explore/dataset/100348)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the parlamentsdienst_grosserrat docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 2, 2),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('parlamentsdienst_grosserrat', default_args=default_args, schedule_interval='0 8/12 * * *',
         catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='parlamentsdienst_grosserrat:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m parlamentsdienst_grosserrat.etl',
        container_name='parlamentsdienst_grosserrat',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
