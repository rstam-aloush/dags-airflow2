"""
# bvb_fahrgastzahlen
This DAG updates the following datasets:

- [100075](https://data.bs.ch/explore/dataset/100075)
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'rstam.aloush',
    'description': 'Run the bvb_fahrgastzahlen docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 4, 26),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('bvb_fahrgastzahlen', default_args=default_args, schedule_interval="*/30 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='bvb_fahrgastzahlen:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m bvb_fahrgastzahlen.etl',
        container_name='bvb_fahrgastzahlen',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/BVB/Fahrgastzahlen",
                      target="/code/data-processing/bvb_fahrgastzahlen/data_orig", type="bind")]
    )
