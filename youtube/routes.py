from flask import Blueprint, jsonify, request
from utils import * 
import re
import sqlite3
import subprocess

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/transcript/<string:video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        transcript = get_youtube_transcript(video_id)
        channel_name = get_youtube_channel_name(video_id)
        words = [word.lower() for word in re.findall(r'\w+', transcript)]

        # Post or get the channel ID from the external database
        channel_id = post_channel_to_external_db(channel_name)

        # Create a dictionary of word counts
        word_counts = {}
        for word in words:
            word_id = post_word_to_external_db(word)
            word_counts[word_id] = word_counts.get(word_id, 0) + 1

        # Post video data to the external database
        post_video_to_external_db(channel_id, video_id, word_counts)

        return jsonify({"transcript": transcript, "channel_name": channel_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@youtube_bp.route('/channel/<string:channel_name>/transcribe', methods=['GET'])
def transcribe_channel_videos(channel_name):
    try:
        # Find the channel ID using the channel name
        channel_id = get_channel_id_from_name(channel_name)

        # Get the recent video IDs for the channel
        video_ids = get_channel_video_ids(channel_id)

        # Transcribe each video and store the results
        transcripts = {}
        for video_id in video_ids:
            transcript = get_youtube_transcript(video_id)
            transcripts[video_id] = transcript

        return jsonify({"transcripts": transcripts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500