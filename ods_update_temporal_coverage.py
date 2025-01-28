"""
# stata_ods/daily_jobs/update_temporal_coverage
This DAG automatically updates the temporal coverage of all datasets

"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'renato.farruggio',
    'description': 'Run the stata_ods/daily_jobs/update_temporal_coverage docker container',
    'depend_on_past': False,
    'start_date': datetime(2024, 10, 25),
    'email': ["jonas.bieri@bs.ch", "orhan.saeedi@bs.ch", "rstam.aloush@bs.ch", "renato.farruggio@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('update_temporal_coverage', default_args=default_args, schedule_interval="0 1 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='update_temporal_coverage:latest',
        api_version='auto',
        auto_remove='force',
        command='python3 -m stata_ods.daily_jobs.update_temporal_coverage.etl',
        container_name='update_temporal_coverage--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        mounts=[Mount(source="/data/dev/workspace/data-processing", target="/code/data-processing", type="bind")]
    )
