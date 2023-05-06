import os
import requests
from datetime import datetime


def split_sku(sku):
    # Splitting the sku for differnt use
    name = sku.split('.')[0]
    c, n = name.split('-')[:2]
    c = c.lower()
    return f"{c}{int(n):05d}", c, n


def get_path(sku):
    return os.path.join(os.getenv("VIDEO_PATH"), sku)


def get_videos_in_dir():
    return [video for video in os.listdir(os.getenv("VIDEO_PATH")) if video.endswith(".mp4")]


def look_at_informer(sku):
    base = os.getenv("INFO_SERVICE")
    data = requests.get(f"{base}/get/{sku}").json()
    return data


def convert_duration(duration):
    try:
        return int(duration)
    except:
        return 0


def convert_release_date(release_date):
    try:
        fmt = '%Y-%m-%d' if len(release_date.split(' ')
                                ) == 1 else '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(release_date, fmt)
    except:
        return datetime.strptime('1999-12-31', '%Y-%m-%d')
