from datetime import timedelta, datetime

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
    "email": ["k.vladimirov@2035.university", ],
    "start_date": airflow.utils.dates.days_ago(2)
}

with DAG(
    "popscience_download_new_info",
    default_args=default_args,
    description="",
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
) as dag:

    update_channel_list = BashOperator(
        task_id='update_channel_list',
        bash_command='python etl/popscience/update_channel_list.py',
    )

    update_playlist_list = BashOperator(
        task_id='update_playlist_list',
        bash_command='python etl/popscience/update_playlist_list.py',
    )

    get_video_info_from_playlists = BashOperator(
        task_id='get_video_info_from_playlists',
        bash_command='python etl/popscience/get_video_info_from_playlists.py',
    )

    update_channel_list >> update_playlist_list >> get_video_info_from_playlists
