import re
import logging
from youtube.utils import get_youtube_transcript, get_youtube_channel_at_tag
import logging
import re
from .external_api import *
import logging
import re
from config import Config
import scrapetube
from concurrent.futures import ThreadPoolExecutor, as_completed
from youtubesearchpython import CustomSearch, VideoSortOrder
# Global cache
cache = {
    "channels": {},
    "videos": set(),
    "words": {},
    "next_word_id": 1
}

# Update cache function
def update_cache_from_external():
    try:
        response = requests.get(f"{Config.EXTERNAL_API_BASE_URL}/all-data", timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        # Populate the cache with the current data from the external API
        cache["channels"] = {channel: None for channel in data.get("channels", [])}
        cache["videos"] = set(data.get("videos", []))
        cache["words"] = {word: i + 1 for i, word in enumerate(data.get("words", []))}
        cache["next_word_id"] = len(data.get("words", [])) + 1
        
        logging.info("Cache updated successfully from external API")
    except requests.RequestException as e:
        logging.error(f"Failed to update cache from external API: {e}")

# Word posting function
def post_words_to_external_db(words):
    # Filter words that are not already in the cache
    new_words = [word for word in words if word not in cache["words"]]
    if not new_words:
        return {}

    try:
        response = requests.post(f"{Config.EXTERNAL_API_BASE_URL}/dictionary", json=new_words, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        word_ids = response.json().get("word_ids", [])
        
        # Update cache with new words
        for word, word_id in zip(new_words, word_ids):
            cache["words"][word] = word_id
        cache["next_word_id"] = max(word_ids) + 1

        return dict(zip(new_words, word_ids))
    except requests.RequestException as e:
        logging.error(f"Error posting words to external database: {e}")
        return {}

def post_channel_to_external_db(channel_name):
    if channel_name in cache["channels"] and cache["channels"][channel_name] is not None:
        return cache["channels"][channel_name]

    try:
        response = requests.post(f"{Config.EXTERNAL_API_BASE_URL}/channel", json={"channel_name": channel_name}, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        channel_id = response.json()['channel_id']
        cache["channels"][channel_name] = channel_id
        return channel_id
    except requests.RequestException as e:
        logging.error(f"Error posting channel to external database: {e}")
        raise

def process_video(video_id):
    if video_id in cache["videos"]:
        logging.info(f"Video ID '{video_id}' already processed. Skipping.")
        return {"status": "Video already processed"}

    try:
        transcript = get_youtube_transcript(video_id)
        channel_name = get_youtube_channel_at_tag(video_id)

        # Extract unique words and convert to lowercase
        words = list(set([word.lower() for word in re.findall(r'\w+', transcript)]))

        # Post the channel name if not already in the cache
        channel_id = post_channel_to_external_db(channel_name)

        # Post words and get their IDs
        word_id_map = post_words_to_external_db(words)

        # Calculate word counts for this video
        word_counts = {}
        for word in words:
            word_id = cache["words"].get(word)
            if word_id is not None:
                word_counts[word_id] = word_counts.get(word_id, 0) + transcript.lower().count(word)

        # Post the video data
        post_video_to_external_db(channel_id, video_id, word_counts)

        # Add the video ID to the cache
        cache["videos"].add(video_id)

        logging.info(f"Successfully processed video ID '{video_id}'.")
        return {"transcript": transcript, "channel_name": channel_name}
    except Exception as e:
        logging.error(f"Error processing video '{video_id}': {e}")
        raise
    
def continuously_process_videos():
    while True:
        try:
            video_ids = fetch_random_youtube_video_ids(count=1)
            for video_id in video_ids:
                if video_id not in cache["videos"]:
                    logging.info(f"Processing video ID '{video_id}'.")
                    result = process_video(video_id)
                    logging.info(f"Result for video ID '{video_id}': {result}")
                    update_cache_from_external()
                else:
                    logging.info(f"Video ID '{video_id}' already processed. Skipping.")
        except Exception as e:
            logging.error(f"Error in continuous video processing: {e}")

def get_channel_video_ids(channel_id):
    videos = scrapetube.get_channel(channel_id)
    video_ids = [video['videoId'] for video in videos]
    return video_ids

def get_channel_id_from_name(channel_name):
    # Search for the channel ID based on channel name
    search_query = f'{channel_name}'
    videos_search = CustomSearch(search_query, VideoSortOrder.relevance, limit=1)
    search_result = videos_search.result()

    if search_result['result']:
        return search_result['result'][0]['channel']['id']
    else:
        raise Exception(f"Unable to find channel ID for '{channel_name}'")

def process_channel_videos(channel_name):
    try:
        # Get the channel ID from the channel name
        channel_id = get_channel_id_from_name(channel_name)
        # Get all video IDs from the channel
        video_ids = get_channel_video_ids(channel_id)

        # Process each video ID
        for video_id in video_ids:
            process_video(video_id)
                
    except Exception as e:
        print(f"Error: {str(e)}")