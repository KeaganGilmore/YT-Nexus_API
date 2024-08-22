import logging
import subprocess
import json
import os
import requests
import re
import sqlite3
from flask import Blueprint, jsonify, request
from utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
EXTERNAL_API_BASE_URL = 'https://lxlibrary.online/yt-nexus/yt-nexus'
REQUEST_TIMEOUT = 10  # Increase this if necessary
MAX_WORKERS = 5  # Number of concurrent workers

youtube_bp = Blueprint('youtube', __name__)

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
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get channel name for video {video_id}: {e}")
        return "Error: Failed to get channel name."
    except Exception as e:
        logging.error(f"An error occurred while getting channel name for video {video_id}: {e}")
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
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to download or process subtitles for video {video_id}: {e}")
        return "Error: Failed to download or process subtitles."
    except FileNotFoundError as e:
        logging.error(f"Subtitle file not found for video {video_id}: {e}")
        return "Error: Subtitle file not found."
    except Exception as e:
        logging.error(f"An error occurred while processing subtitles for video {video_id}: {e}")
        return f"An error occurred: {str(e)}"

def post_word_to_external_db(word):
    start_time = time()
    try:
        logging.debug(f"Posting word '{word}' to external database. [Started at {start_time:.2f}s]")
        response = requests.post(f"{EXTERNAL_API_BASE_URL}/dictionary", json={"word": word}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        word_id = response.json()["word_id"]
        end_time = time()
        logging.debug(f"Received word ID '{word_id}' for word '{word}'. [Completed at {end_time:.2f}s, Duration: {end_time - start_time:.2f}s]")
        return word, word_id
    except requests.RequestException as e:
        logging.error(f"Error posting word '{word}' to external database: {e}")
        return word, None

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

