"""
# pull_repo_changes
This DAG pulls recent changes from the main/master branch of the following repositories:

- [data-processing](https://github.com/opendatabs/data-processing)
- [dags-airflow2](https://github.com/opendatabs/dags-airflow2)
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run the bash script to pull changes',
    'depend_on_past': False,
    'start_date': datetime(2024, 4, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
}

with DAG('pull_repo_changes', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    pull_changes = BashOperator(
        task_id='pull_repo_changes',
        bash_command='bash -c /data/dev/workspace/pull_changes.sh '
    )
