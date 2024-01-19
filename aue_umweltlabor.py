"""
# aue-umweltlabor
This DAG updates the following datasets:

- [100066](https://data.bs.ch/explore/dataset/100066)
- [100067](https://data.bs.ch/explore/dataset/100067)
- [100068](https://data.bs.ch/explore/dataset/100068)
- [100069](https://data.bs.ch/explore/dataset/100069)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the aue-umweltlabor docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 19),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=30)
}

with DAG('aue_umweltlabor', default_args=default_args, schedule_interval="0 6 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='aue-umweltlabor:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m aue_umweltlabor.etl',
        container_name='aue-umweltlabor',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[
            {
                "Source": "/data/dev/workspace/data-processing",
                "Target": "/code/data-processing",
                "Type": "bind",
                "ReadOnly": False
            },
            {
                "Source": "/mnt/OGD-DataExch/Umweltlabor",
                "Target": "/code/data-processing/aue_umweltlabor/data_orig",
                "Type": "bind",
                "ReadOnly": False
            }]
    )

    ods_publish = DockerOperator(
        task_id='ods-publish',
        image='ods-publish:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m ods_publish.etl_id 100066,100067,100068,100069',
        container_name='aue-umweltlabor--ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[
            {
                "Source": "/data/dev/workspace/data-processing",
                "Target": "/code/data-processing",
                "Type": "bind",
                "ReadOnly": False
            }]
    )

    process_upload >> ods_publish
