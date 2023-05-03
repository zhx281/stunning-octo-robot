import os
import requests


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


# External Parser
def look_at_informer(sku):
    base = os.getenv("INFO_SERVICE")
    data = requests.get(f"{base}/get/{sku}").json()
    return data
