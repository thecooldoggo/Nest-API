import os
import json
import requests
import threading
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
api_key = "REDACTED"
data_directory = "pub"

if not os.path.exists(data_directory):
    os.makedirs(data_directory)

def fetch_and_store_stats(channel_id, user_id):
    try:
        while True:
            print(f"Fetching stats for channel_id: {channel_id}")
            url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
            response = requests.get(url)
            data = response.json()
            if "items" not in data or not data["items"]:
                print(f"No data found for channel_id: {channel_id}")
                time.sleep(1200)
                continue

            stats = data['items'][0]['statistics']
            subscriber_count = stats.get('subscriberCount', 'N/A')
            view_count = stats.get('viewCount', 'N/A')
            data = {
                "subscriber_count": subscriber_count,
                "view_count": view_count
            }
            file_path = os.path.join(data_directory, f"yt-stats-{user_id}.json")
            with open(file_path, 'w') as file:
                json.dump(data, file)
                print(f"Data written to {file_path}")
            time.sleep(1200)
    except Exception as e:
        print(f"Error fetching stats: {e}")

@app.route('/api/add-channel', methods=['POST'])
def add_channel():
    data = request.json
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    if not channel_id or not user_id:
        return jsonify({"error": "Missing channel_id or user_id"}), 400

    print(f"Received request to add channel_id: {channel_id} for user_id: {user_id}")
    threading.Thread(target=fetch_and_store_stats, args=(channel_id, user_id)).start()
    return jsonify({"message": "Channel added successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53433, debug=False)
