import logging
import requests
from flask import Blueprint, jsonify, request
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
import random
from pytube import Search
# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
EXTERNAL_API_BASE_URL = 'https://lxlibrary.online/yt-nexus'
REQUEST_TIMEOUT = 10  # Increase this if necessary
MAX_WORKERS = 5  # Number of concurrent workers

youtube_bp = Blueprint('youtube', __name__)

def post_words_to_external_db(words):
    start_time = time()
    try:
        logging.debug(f"Posting words '{words}' to external database. [Started at {start_time:.2f}s]")
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/dictionary", json=words, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        word_ids = response.json()["word_ids"]
        end_time = time()
        logging.debug(f"Received word IDs '{word_ids}' for words '{words}'. [Completed at {end_time:.2f}s, Duration: {end_time - start_time:.2f}s]")
        # Map the words to their corresponding word_ids
        return dict(zip(words, word_ids))
    except requests.RequestException as e:
        logging.error(f"Error posting words '{words}' to external database: {e}")
        return {}

def post_channel_to_external_db(channel_name):
    try:
        logging.debug(f"Posting channel '{channel_name}' to external database.")
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/channel", json={"channel_name": channel_name}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        channel_id = response.json()['channel_id']
        logging.debug(f"Received channel ID '{channel_id}' for channel '{channel_name}'.")
        return channel_id
    except requests.RequestException as e:
        logging.error(f"Error posting channel '{channel_name}' to external database: {e}")
        raise

def post_video_to_external_db(channel_id, video_id, word_counts):
    try:
        logging.debug(f"Posting video '{video_id}' with channel_id '{channel_id}' to external database.")
        data = {
            "channel_id": channel_id,
            "video_id": video_id,
            "word_counts": word_counts
        }
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/video", json=data, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logging.debug(f"Successfully posted video '{video_id}'.")
    except requests.RequestException as e:
        logging.error(f"Error posting video '{video_id}' to external database: {e}")
        raise

def fetch_random_youtube_video_ids(count=1):
    """
    Fetches a specified number of random YouTube video IDs.
    
    :param count: The number of random video IDs to fetch.
    :return: List of random YouTube video IDs.
    """
    random_search_terms = [
        "funny videos", "music videos", "tech reviews", 
        "news", "gaming", "travel vlogs", "tutorials"
    ]
    
    video_ids = []
    for _ in range(count):
        search_term = random.choice(random_search_terms)
        search = Search(search_term)
        video = random.choice(search.results)
        video_ids.append(video.video_id)
    
    return video_ids