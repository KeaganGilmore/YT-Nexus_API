import subprocess
import json
import os
from youtubesearchpython import CustomSearch, VideoSortOrder
import scrapetube
import requests
def get_youtube_channel_name(video_id):
    try:
        command = [
            'yt-dlp',
            '--skip-download',
            '--no-warnings',
            '--no-simulate',
            '--get-filename',
            '--output', '%(channel)s',
            f'https://www.youtube.com/watch?v={video_id}'
        ]
        output = subprocess.check_output(command, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError:
        return "Error: Failed to get channel name."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_youtube_transcript(video_id):
    try:
        command = [
            'yt-dlp',
            '--skip-download',
            '--no-warnings',
            '--no-simulate',
            '--write-subs',
            '--write-auto-subs',
            '--sub-format', 'json3',
            '--sub-langs', 'en',
            '--output', '%(id)s',
            f'https://www.youtube.com/watch?v={video_id}'
        ]
        subprocess.run(command, check=True)
        transcript_file = f"{video_id}.en.json3"
        with open(transcript_file, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)
        transcript = ''
        for event in transcript_data['events']:
            if 'segs' in event:
                for seg in event['segs']:
                    transcript += seg['utf8']
        os.remove(transcript_file)
        return transcript.strip()
    except subprocess.CalledProcessError:
        return "Error: Failed to download or process subtitles."
    except FileNotFoundError:
        return "Error: Subtitle file not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def get_recent_videos_by_channel(channel_name):
    # Prepare the search query with the channel name
    search_query = f'{channel_name}'

    video_ids = []
    next_page_token = None

    while True:
        # Perform the search
        videos_search = CustomSearch(search_query, VideoSortOrder.uploadDate, limit=20)
        search_result = videos_search.result()

        if not search_result['result']:
            break

        for video in search_result['result']:
            # Filter by channel name to ensure the video is from the correct channel
            if video['channel']['name'] == channel_name:
                video_ids.append(video['id'])

        # Check if there's a next page
        if 'continuation' in search_result:
            next_page_token = search_result['continuation']
        else:
            break

    return video_ids

def get_channel_video_ids(channel_id):
    videos = scrapetube.get_channel(channel_id)
    video_ids = [video['videoId'] for video in videos]
    return video_ids

def get_channel_id_from_name(channel_name):
    search_query = f'{channel_name}'
    videos_search = CustomSearch(search_query, VideoSortOrder.relevance, limit=1)
    search_result = videos_search.result()

    if search_result['result']:
        return search_result['result'][0]['channel']['id']
    else:
        raise Exception(f"Unable to find channel ID for '{channel_name}'")
    
EXTERNAL_API_BASE_URL = 'http://localhost:8110/yt-nexus'

def post_word_to_external_db(word):
    try:
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/dictionary", json={"word": word})
        response.raise_for_status()
        return response.json()["word_id"]
    except requests.RequestException as e:
        print(f"Error posting word to external database: {e}")
        raise

def post_channel_to_external_db(channel_name):
    try:
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/channel", json={"channel_name": channel_name})
        response.raise_for_status()
        return response.json()['channel_id']
    except requests.RequestException as e:
        print(f"Error posting channel to external database: {e}")
        raise

def post_video_to_external_db(channel_id, video_id, word_counts):
    try:
        data = {
            "channel_id": channel_id,
            "video_id": video_id,
            "word_counts": word_counts
        }
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/video", json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error posting video to external database: {e}")
        raise
    
def fetch_videos_by_keyword(channel_name, keyword):
    try:
        response = requests.get(f"{EXTERNAL_API_BASE_URL}/channel/{channel_name}/keyword/{keyword}")
        response.raise_for_status()
        return response.json()["videos"]
    except requests.RequestException as e:
        print(f"Error fetching videos with keyword from external database: {e}")
        raise
    
def fetch_top_videos_by_channel(channel_name):
    try:
        response = requests.get(f"{EXTERNAL_API_BASE_URL}/channel/{channel_name}/top-videos")
        response.raise_for_status()
        return response.json()["top_videos"]
    except requests.RequestException as e:
        print(f"Error fetching top videos from external database: {e}")
        raise
    
def fetch_common_words_by_channel(channel_name):
    try:
        response = requests.get(f"{EXTERNAL_API_BASE_URL}/channel/{channel_name}/common-words")
        response.raise_for_status()
        return response.json()["common_words"]
    except requests.RequestException as e:
        print(f"Error fetching common words from external database: {e}")
        raise