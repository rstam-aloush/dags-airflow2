"""
# iwb_gas.py
This DAG updates the following datasets:

- [100304](https://data.bs.ch/explore/dataset/100304)
- [100358](https://data.bs.ch/explore/dataset/100358)

"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the iwb_gas.py docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 26),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('iwb_gas', default_args=default_args, schedule_interval="0 13 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='iwb_gas:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m iwb_gas.etl',
        container_name='iwb_gas--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )

    fit_model = DockerOperator(
        task_id='fit_model',
        image='gasverbrauch:latest',
        api_version='auto',
        auto_remove='force',
        command='Rscript /code/data-processing/stata_erwarteter_gasverbrauch/Gasverbrauch_OGD.R',
        container_name='gasverbrauch--fit_model',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Gasverbrauch",
                      target="/code/data-processing/stata_erwarteter_gasverbrauch/data/export", type="bind")]
    )

    upload >> fit_model
