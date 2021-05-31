from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.popscience.utils import workflow


dag = DAG('new_orders',
          schedule_interval=timedelta(hours=6),
          # Дата start_date обязательно должна быть в прошлом,
          # иначе не будет статусов у задач
          # Должен быть запущен airflow scheduler
          start_date=datetime(2021, 5, 31, 0))


def workflow1(**context):
    print("Hello from DAG:workflow")
    print(context)


tasks = []
for i in range(5):
    tasks.append(PythonOperator(
        task_id=f"task_{i}",
        python_callable=workflow1,
        provide_context=True,
        dag=dag))

import_task = PythonOperator(
    task_id=f"import_task",
    python_callable=workflow,
    provide_context=True,
    dag=dag)


tasks[2] >> import_task
