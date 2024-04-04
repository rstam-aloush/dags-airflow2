"""
# pull_repo_changes
This DAG pulls recent changes from the main/master branch of the following repositories:

- [data-processing](https://github.com/opendatabs/data-processing)
- [dags-airflow2](https://github.com/opendatabs/dags-airflow2)
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import git


def pull_repo(repo_path):
    try:
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        return f'Successfully pulled {repo_path}'
    except Exception as e:
        return f'Failed to pull {repo_path}: {str(e)}'


default_args = {
    'owner': 'orhan.saeedi',
    'description': 'Run git pull on multiple repositories',
    'depend_on_past': False,
    'start_date': datetime(2024, 4, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
}

with DAG('git_pull_repos', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    pull_data_processing = PythonOperator(
        task_id='pull_data_processing',
        python_callable=pull_repo,
        op_kwargs={'repo_path': '/data/dev/workspace/data-processing'},
    )

    pull_dags_airflow2 = PythonOperator(
        task_id='pull_dags_airflow2',
        python_callable=pull_repo,
        op_kwargs={'repo_path': '/data/dev/workspace/dags-airflow2'},
    )
