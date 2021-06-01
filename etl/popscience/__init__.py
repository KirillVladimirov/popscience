from sqlalchemy.dialects.postgresql import insert
from etl.schema import engine
from etl.schema import YoutubeChannel
from etl.schema import YoutubePlaylist
from etl.schema import Session

from tqdm import tqdm

from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoPrivate
from pytube.exceptions import VideoUnavailable

import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException

from urllib.error import URLError


def update_channel_list():
    """
    Сохранение в БД списка каналов
    :return:
    """
    with open('./data/channels_list.txt') as f:
        channels_list = f.read().splitlines()
    channels_list = list(set(channels_list))
    print("LEN:", len(channels_list))

    with engine.connect() as conn:
        stmt = insert(YoutubeChannel).values([
            {"url": channel} for channel in channels_list
        ]).on_conflict_do_nothing()
        conn.execute(stmt)
    return


def update_playlist_list():
    session = Session()
    channels = session.query(YoutubeChannel).all()
    print(len(channels), channels[0].url)

    playlist_ids = []

    for channel in tqdm(channels[:5]):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(channel.url+"/playlists?view=1&sort=dd&shelf_id=0")
        time.sleep(5)
        height = driver.execute_script("return document.documentElement.scrollHeight")
        lastheight = 0

        # Прокручиваем страницу вниз до конца
        while True:
            if lastheight == height:
                break
            lastheight = height
            driver.execute_script("window.scrollTo(0, " + str(height) + ");")
            time.sleep(2)
            height = driver.execute_script("return document.documentElement.scrollHeight")

        user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
        for i in user_data:
            url = i.get_attribute('href')
            playlist_id = url.split("=")[-1]
            playlist_ids.append(playlist_id)
            with engine.connect() as conn:
                stmt = insert(YoutubePlaylist).values(youtube_id=playlist_id).on_conflict_do_nothing()
                conn.execute(stmt)

        driver.close()
        driver.quit()

    # sleep = 3
    # URLError_counter = 0
    # engine = create_engine("postgresql://postgres:@localhost:5432/university2035_etl", echo=True)
    #
    # for playlist_id in tqdm(channels):
    #     try:
    #         playlist = f"https://www.youtube.com/playlist?list={playlist_id}"
    #
    #         # Получение информации о плейлисте
    #         driver = webdriver.Chrome('../chromedriver')
    #         driver.get(playlist)
    #         time.sleep(sleep)
    #         user_data = driver.find_elements_by_xpath('//*[@id="description"]')
    #         pl_description = user_data[0].text
    #         user_data = driver.find_elements_by_xpath("//*[contains(text(), 'views')]")
    #         pl_views = user_data[1].text
    #         digits = [s for s in pl_views.split()[0] if s.isdigit()]
    #         if len(digits) == 0:
    #             pl_views = 0
    #         else:
    #             pl_views = int("".join(digits))
    #         driver.close()
    #         #         driver.quit()
    #         p = Playlist(playlist)
    #         pl_title = p.title
    #
    #         for url in p.video_urls:
    #             for i in range(10):
    #                 try:
    #                     # jon_tutorial = collection.find_one({"origin_url": url})
    #                     # if jon_tutorial is not None:
    #                     #     break
    #
    #                     info = {}
    #                     try:
    #                         yt = YouTube(url)
    #                     except VideoPrivate:
    #                         print(f"Private video {url}")
    #                         break
    #                     except VideoUnavailable:
    #                         print(f"Unavailable video {url}")
    #                         break
    #                     info["title"] = yt.title
    #                     info["playlist_title"] = pl_title
    #                     info["playlist_description"] = pl_description
    #                     info["playlist_views"] = pl_views
    #                     info["date"] = yt.publish_date
    #                     info["origin_url"] = url
    #                     info["views"] = yt.views
    #                     info["duation"] = yt.length
    #                     info["author"] = yt.author
    #                     info["tags"] = yt.keywords
    #                     info["about"] = yt.description
    #                     info["rating"] = yt.rating
    #                     info["platform"] = "YouTube"
    #                     info["theme"] = yt.thumbnail_url
    #                     if yt.captions.get("ru") is not None:
    #                         caption = yt.captions.get('ru')
    #                         info["language"] = "ru"
    #                     elif yt.captions.get("a.ru") is not None:
    #                         caption = yt.captions.get('a.ru')
    #                         info["language"] = "a.ru"
    #                     if caption:
    #                         info["captions_xml"] = caption.xml_captions
    #                         info["captions_str"] = caption.generate_srt_captions()
    #                     result = collection.insert_one(info)
    #                 except DuplicateKeyError:
    #                     print("============ DuplicateKeyError ============")
    #                     #                     traceback.print_exc()
    #                     continue
    #                 except URLError:
    #                     print("============ URLError ============")
    #                     traceback.print_exc()
    #                     URLError_counter += 1
    #                     if URLError_counter == 20:
    #                         URLError_counter = 0
    #                         break
    #                     time.sleep(sleep)
    #                     continue
    #                 except KeyError:
    #                     print("============ KeyError ============")
    #                     break
    #                 else:
    #                     break
    #     except KeyboardInterrupt:
    #         print("============ KeyboardInterrupt ============")
    #         break
    #     except:
    #         print("============ UnnounError ============")
    #         traceback.print_exc()
    #         continue


def get_video_info_from_playlists():
    print("RUN get_video_info_from_playlists")
    # channels = youtube_channels.query.all()
    # sleep = 3
    # URLError_counter = 0
    # engine = create_engine("postgresql://postgres:@localhost:5432/university2035_etl", echo=True)
    #
    # for playlist_id in tqdm(channels):
    #     try:
    #         playlist = f"https://www.youtube.com/playlist?list={playlist_id}"
    #
    #         # Получение информации о плейлисте
    #         driver = webdriver.Chrome('../chromedriver')
    #         driver.get(playlist)
    #         time.sleep(sleep)
    #         user_data = driver.find_elements_by_xpath('//*[@id="description"]')
    #         pl_description = user_data[0].text
    #         user_data = driver.find_elements_by_xpath("//*[contains(text(), 'views')]")
    #         pl_views = user_data[1].text
    #         digits = [s for s in pl_views.split()[0] if s.isdigit()]
    #         if len(digits) == 0:
    #             pl_views = 0
    #         else:
    #             pl_views = int("".join(digits))
    #         driver.close()
    #         #         driver.quit()
    #         p = Playlist(playlist)
    #         pl_title = p.title
    #
    #         for url in p.video_urls:
    #             for i in range(10):
    #                 try:
    #                     # jon_tutorial = collection.find_one({"origin_url": url})
    #                     # if jon_tutorial is not None:
    #                     #     break
    #
    #                     info = {}
    #                     try:
    #                         yt = YouTube(url)
    #                     except VideoPrivate:
    #                         print(f"Private video {url}")
    #                         break
    #                     except VideoUnavailable:
    #                         print(f"Unavailable video {url}")
    #                         break
    #                     info["title"] = yt.title
    #                     info["playlist_title"] = pl_title
    #                     info["playlist_description"] = pl_description
    #                     info["playlist_views"] = pl_views
    #                     info["date"] = yt.publish_date
    #                     info["origin_url"] = url
    #                     info["views"] = yt.views
    #                     info["duation"] = yt.length
    #                     info["author"] = yt.author
    #                     info["tags"] = yt.keywords
    #                     info["about"] = yt.description
    #                     info["rating"] = yt.rating
    #                     info["platform"] = "YouTube"
    #                     info["theme"] = yt.thumbnail_url
    #                     if yt.captions.get("ru") is not None:
    #                         caption = yt.captions.get('ru')
    #                         info["language"] = "ru"
    #                     elif yt.captions.get("a.ru") is not None:
    #                         caption = yt.captions.get('a.ru')
    #                         info["language"] = "a.ru"
    #                     if caption:
    #                         info["captions_xml"] = caption.xml_captions
    #                         info["captions_str"] = caption.generate_srt_captions()
    #                     result = collection.insert_one(info)
    #                 except DuplicateKeyError:
    #                     print("============ DuplicateKeyError ============")
    #                     #                     traceback.print_exc()
    #                     continue
    #                 except URLError:
    #                     print("============ URLError ============")
    #                     traceback.print_exc()
    #                     URLError_counter += 1
    #                     if URLError_counter == 20:
    #                         URLError_counter = 0
    #                         break
    #                     time.sleep(sleep)
    #                     continue
    #                 except KeyError:
    #                     print("============ KeyError ============")
    #                     break
    #                 else:
    #                     break
    #     except KeyboardInterrupt:
    #         print("============ KeyboardInterrupt ============")
    #         break
    #     except:
    #         print("============ UnnounError ============")
    #         traceback.print_exc()
    #         continue



















