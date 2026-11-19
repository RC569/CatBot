import requests
import json
import os

from pprint import pprint

# Settings
koito_base_url = "http://135.148.166.11:62250"
koito_now_playing = "/apis/web/v1/now-playing"
koito_api_key = os.getenv("KOITO_APIKEY")
KOITO_AUTH_HEADER = {
    "Authorization": f"Token {koito_api_key}"
}

def get_current_track():
    r = requests.get(koito_base_url + koito_now_playing, headers=KOITO_AUTH_HEADER)
    if r.status_code == 200:
        data = r.json()
        
        title = data["track"]["title"]
        artist = data["track"]["artists"][0]["name"]

        pprint(data)
        print(data["currently_playing"]) # add something for when this is False
        print(f"RC is Listening to **{title}** by **{artist}**")
    else:
        print("It's over")

get_current_track()
