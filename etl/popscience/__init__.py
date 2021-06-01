from sqlalchemy.dialects.postgresql import insert
from etl.schema import engine
from etl.schema import YoutubeChannel
from etl.schema import YoutubePlaylist
from etl.schema import YoutubeVideo
from etl.schema import Session

from pytube import YouTube
from pytube import Playlist
from selenium import webdriver
from pytube.exceptions import VideoPrivate
from pytube.exceptions import VideoUnavailable
from urllib.error import URLError

import time
import traceback


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

    for channel in channels[:5]:
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
            with engine.connect() as conn:
                stmt = insert(YoutubePlaylist) \
                    .values(youtube_id=playlist_id, channel_id=channel.id).on_conflict_do_nothing()
                conn.execute(stmt)

        driver.close()
        driver.quit()
    session.commit()


def get_playlist_info():
    session = Session()
    playlists = session.query(YoutubePlaylist).all()
    print(playlists[0].youtube_id)
    print(playlists[0].channel_id)
    sleep = 3

    for playlist in playlists:
        playlist_url = f"https://www.youtube.com/playlist?list={playlist.youtube_id}"
        print(playlist_url)
        # Получение информации о плейлисте
        driver = webdriver.Chrome('./chromedriver')
        driver.get(playlist_url)
        time.sleep(sleep)
        user_data = driver.find_elements_by_xpath('//*[@id="description"]')
        pl_description = user_data[0].text
        user_data = driver.find_elements_by_xpath("//*[contains(text(), 'views')]")
        pl_views = user_data[1].text
        print("pl_description", pl_description)
        print("pl_views", pl_views)

        digits = [s for s in pl_views.split()[0] if s.isdigit()]
        if len(digits) == 0:
            pl_views = 0
        else:
            pl_views = int("".join(digits))
        driver.close()
        p = Playlist(playlist_url)
        pl_title = p.title
        print("pl_title", pl_title)
        playlist.title = pl_title
        playlist.description = pl_description
        playlist.views = pl_views
        session.commit()


def get_video_info_from_playlists():
    session = Session()
    playlists = session.query(YoutubePlaylist).all()
    sleep = 3
    URLError_counter = 0
    print("PLAYLIST COUNT:", len(playlists))

    for playlist in playlists:
        try:
            playlist_url = f"https://www.youtube.com/playlist?list={playlist.youtube_id}"
            p = Playlist(playlist_url)
            print("VIDEOS COUNT:", len(p.video_urls))
            for url in p.video_urls:
                for i in range(10):
                    videos = session.query(YoutubeVideo).filter(YoutubeVideo.origin_url == url).all()
                    if len(videos) > 0:
                        print("duplicate video:", url)
                        break
                    yt = YouTube(url)
                    video = YoutubeVideo()
                    video.channel_id = playlist.channel_id
                    video.playlist_id = playlist.id
                    video.origin_url = url
                    video.title = yt.title
                    video.date = yt.publish_date
                    video.duration = yt.length
                    video.author = yt.author
                    video.tags = yt.keywords
                    video.about = yt.description
                    video.rating = yt.rating
                    video.views = yt.views
                    video.theme = yt.thumbnail_url
                    caption = None
                    if yt.captions.get("ru") is not None:
                        caption = yt.captions.get('ru')
                        video.language = "ru"
                    elif yt.captions.get("a.ru") is not None:
                        caption = yt.captions.get('a.ru')
                        video.language = "a.ru"
                    if caption:
                        video.captions_xml = caption.xml_captions
                    session.add(video)
                    session.commit()
                    print("save video")
        except VideoPrivate:
            print(f"Private video {url}")
            break
        except VideoUnavailable:
            print(f"Unavailable video {url}")
            break
        except URLError:
            print("============ URLError ============")
            traceback.print_exc()
            URLError_counter += 1
            if URLError_counter == 20:
                URLError_counter = 0
                break
            time.sleep(sleep)
            continue
        except:
            print("============ UnnounError ============")
            traceback.print_exc()
            continue
