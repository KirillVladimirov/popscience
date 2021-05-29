from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from tqdm.notebook import tqdm
from sqlalchemy import create_engine
from etl.schema import metadata, youtube_channels
import traceback
import pickle


def main():
    with open('../../data/channels_list.txt') as f:
        channels_list = f.read().splitlines()
    channels_list = list(set(channels_list))
    print(channels_list)
    engine = create_engine("postgresql://postgres:@localhost:5432/university2035_etl", echo=True)

    with engine.connect() as conn:
        query = youtube_channels.insert().values(
            url="https://www.youtube.com/watch?v=KFj3VhMTAdk&ab_channel=MoscowPython"
        ).returning(youtube_channels)
        data = conn.execute(query).fetchone()

    # with engine.connect() as conn:
    #     query = youtube_channels.insert().values([
    #         {"url": channel} for channel in channels_list
    #     ]).returning(youtube_channels)
    #     print(query.compile(engine))
    #     data = conn.execute(query).fetchall()
    return 0


if __name__ == "__main__":
    main()

