from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta, date

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 5, 28),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('google_timeline_ingestion', description='daily ingestion for google timeline data',
          default_args=default_args, schedule_interval='0 3 * * *', catchup=False)

t_1 = DockerOperator(
    task_id='initialize_raw_staging',
    image='tracker-task1',
    api_version='auto',
    auto_remove=True,
    command="python /usr/timeline_tracker/tasks/task_initialize_raw_staging.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    dag=dag
)

t_2 = DockerOperator(
    task_id='extract_raw_to_staging',
    image='tracker-task1',
    api_version='auto',
    auto_remove=True,
    command="python /usr/timeline_tracker/tasks/task_extract_raw_to_staging.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    dag=dag
)

t_3 = DockerOperator(
    task_id='initialize_target',
    image='tracker-task1',
    api_version='auto',
    auto_remove=True,
    command="python /usr/timeline_tracker/tasks/task_initialize_target_table.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    dag=dag
)

t_4 = DockerOperator(
    task_id='initialize_dates',
    image='tracker-task1',
    api_version='auto',
    auto_remove=True,
    command="python /usr/timeline_tracker/tasks/task_initialize_dates_table.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    dag=dag
)

t_5 = DockerOperator(
    task_id='transform_data',
    image='tracker-task1',
    api_version='auto',
    auto_remove=True,
    command="python /usr/timeline_tracker/tasks/task_transform_data.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    dag=dag
)

t_6 = DockerOperator(
    task_id='clear_staging',
    image='tracker-task1',
    api_version='auto',
    auto_remove=True,
    command="python /usr/timeline_tracker/tasks/task_clear_staging.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    dag=dag
)

t_1 >> t_2 >> t_3 >> t_4 >> t_5 >> t_6
