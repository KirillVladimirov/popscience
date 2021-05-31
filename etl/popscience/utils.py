import time


def workflow(**context):
    print("Hello from new module workflow")
    print(context)


def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)
