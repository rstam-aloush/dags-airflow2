"""
# esc_faq.py
This DAG updates the following datasets:

- [100417](https://data.bs.ch/explore/dataset/100417)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the esc_faq docker container',
    'depend_on_past': False,
    'start_date': datetime(2025, 1, 31),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('esc_faq', default_args=default_args, schedule_interval='*/5 * * * *',
         catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='esc_faq:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m esc_faq.etl',
        container_name='esc_faq',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/PD-ESC-FAQ/FAQs",
                      target="/code/data-processing/esc_faq/data_orig", type="bind")]
    )
