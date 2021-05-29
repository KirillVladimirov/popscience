
1. Миграции в Alembic

в файле alembic.ini нужно настроить доступ к БД
sqlalchemy.url = postgresql://postgres:@localhost:5432/university2035_etl

файлы миграций храняться в ./alembic/versions/

При описании таблицы в файле ./etl/schema.py можно сгенерировать код миграции
alembic revision --message="Comment" --autogenerate

Применение миграции 
alembic upgrade head

откат миграции
alembic downgrade 79ab43cbd198

откатить все миграции 
alembic downgrade -1


2. Airflow
Обязательно установить переменную окружения AIRFLOW_HOME на дерикторию проекта
export AIRFLOW_HOME=./
   
Запуск сервисов Airflow
airflow webserver
airflow scheduler

Скрипты с описанием задач находятся в ./dags
Если все верно, то название ДАГА должно отображаться в интерфейсе (например popscience_download_new_info)
```bazaar
with DAG(
    "popscience_download_new_info",
    default_args=default_args,
    description="",
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
```

операторы описываются как BashOperator который просто запускает python скрипт

Все скрипты находятся в ./etl/


