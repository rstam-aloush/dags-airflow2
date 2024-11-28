"""
# stata_konoer.py


"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the stata_konoer docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 11, 28),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch",
              "nicolas.maire@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}
with DAG('iwb_gas', default_args=default_args, schedule_interval="0 10 * * *", catchup=False) as dag:
    transform = DockerOperator(
            task_id='transform',
            image='stata_konoer:latest',
            api_version='auto',
            auto_remove='force',
            command='Rscript /code/data-processing/stata_konoer/etl.R',
            container_name='stata_konoer--transform',
            docker_url="unix://var/run/docker.sock",
            network_mode="bridge",
            tty=True,
            mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                    Mount(source="/mnt/OGD-DataExch/StatA/KoNör",
                          target="/code/data-processing/stata_konoer/data", type="bind")]
        )
