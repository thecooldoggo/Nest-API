import os
import json
import requests
import time

api_key = "API-KEY"
channel_id = "Channel ID"

def get_youtube_stats(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    stats = data['items'][0]['statistics']
    subscriber_count = stats['subscriberCount']
    view_count = stats['viewCount']
    return subscriber_count, view_count

while True:
    subscriber_count, view_count = get_youtube_stats(channel_id)
    data = {
        "subscriber_count": subscriber_count,
        "view_count": view_count
    }
    with open('pub/yt-stats.json', 'w') as file:
        json.dump(data, file)
        print("Data written to file")
    time.sleep(1200)
