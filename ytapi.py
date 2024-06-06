import os
import json
import requests
import time
import traceback

api_key = "API-KEY"
channel_id = "Channel ID"
error_log_file = "error_log_ytapi.txt"
# error logging
def log_error(error_message):
    with open(error_log_file, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")

def get_youtube_stats(channel_id):
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        stats = data['items'][0]['statistics']
        subscriber_count = stats['subscriberCount']
        view_count = stats['viewCount']
        return subscriber_count, view_count
    except Exception as e:
        log_error(traceback.format_exc())
        return None, None

while True:
    try:
        subscriber_count, view_count = get_youtube_stats(channel_id)
        if subscriber_count is not None and view_count is not None:
            data = {
                "subscriber_count": subscriber_count,
                "view_count": view_count
            }
            with open('pub/yt-stats.json', 'w') as file:
                json.dump(data, file)
                print("Data written to file")
        else:
            print("Failed to retrieve YouTube stats")
    except Exception as e:
        log_error(traceback.format_exc())
    
    time.sleep(1200)
