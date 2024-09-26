"""
# iwb_netzlast.py
This DAG updates the following datasets:

- [100233](https://data.bs.ch/explore/dataset/100233)
- [100245](https://data.bs.ch/explore/dataset/100245)
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the iwb_netzlast.py docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 25),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch",
              "nicolas.maire@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('iwb_netzlast', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='iwb_netzlast:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m iwb_netzlast.etl',
        container_name='iwb_netzlast--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/IWB/Netzlast", target="/code/data-processing/iwb_netzlast/data",
                      type="bind")]
    )

    fit_model = DockerOperator(
        task_id='fit_model',
        image='stromverbrauch:latest',
        api_version='auto',
        auto_remove='force',
        command='Rscript /code/data-processing/stata_erwarteter_stromverbrauch/Stromverbrauch_OGD.R',
        container_name='stromverbrauch--fit_model',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind"),
                Mount(source="/mnt/OGD-DataExch/StatA/Stromverbrauch",
                      target="/code/data-processing/stata_erwarteter_stromverbrauch/data/export", type="bind")]
    )

    upload >> fit_model
