import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from etl.popscience import update_channel_list
from etl.popscience import update_playlist_list
from etl.popscience import get_video_info_from_playlists
from etl.popscience import get_playlist_info

from datetime import timedelta, datetime


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
    start_date=datetime(2021, 5, 31, 0),
) as dag:

    update_channel_list = PythonOperator(
        task_id="update_channel_list",
        python_callable=update_channel_list,
        provide_context=True,
    )

    # update_playlist_list = PythonOperator(
    #     task_id="update_playlist_list",
    #     python_callable=update_playlist_list,
    #     provide_context=True,
    # )

    # get_playlist_info = PythonOperator(
    #     task_id="get_playlist_info",
    #     python_callable=get_playlist_info,
    #     provide_context=True,
    # )

    get_video_info_from_playlists = PythonOperator(
        task_id="get_video_info_from_playlists",
        python_callable=get_video_info_from_playlists,
        provide_context=True,
    )

    # update_channel_list >> update_playlist_list >> get_video_info_from_playlists
    # update_channel_list >> update_playlist_list
    # update_channel_list >> get_playlist_info
    update_channel_list >> get_video_info_from_playlists
