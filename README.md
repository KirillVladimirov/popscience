
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

откатить миграцию назад
alembic downgrade -1


2. Airflow 

Обязательно установить переменную окружения AIRFLOW_HOME на дерикторию проекта
export AIRFLOW_HOME=./
   
Чтобы модули с функциями были доступны в airflow%
export PYTHONPATH=./etl/:$PYTHONPATH

Запуск сервисов Airflow
- airflow webserver
- airflow scheduler

Скрипты с описанием последовательности задач находятся в ./dags
Скрипты с кодом задач находятся в ./etl
Для popscience - ./etl/popscience
Модели для БД будут все в одном файле ./etl/schema.py

Если все верно, то название ДАГА должно отображаться в интерфейсе (например popscience_download_new_info)

операторы описываются как PythonOperator который просто запускает функцию



Информация:
- [Apache Airflow: делаем ETL проще](https://habr.com/ru/post/512386/) большой туториал
- [Data pipelines, Luigi, Airflow: everything you need to know](https://towardsdatascience.com/data-pipelines-luigi-airflow-everything-you-need-to-know-18dc741449b7) Сравнение airflow и Luigi
- [Airflow: a workflow management platform](https://medium.com/airbnb-engineering/airflow-a-workflow-management-platform-46318b977fd8) обзор Airflow от разработчика Airbnb
- [Getting started with Apache Airflow](https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b)
- [Airflow и MLFlow автоматизаций пайплайнов Machine Learning / MLOps](https://www.youtube.com/watch?v=NfPf0Y770DA)
- [Apache Airflow Tutorials](https://www.youtube.com/playlist?list=PLYizQ5FvN6pvIOcOd6dFZu3lQqc6zBGp2)
