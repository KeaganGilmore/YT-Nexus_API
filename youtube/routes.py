from flask import Blueprint, jsonify, request
from utils import * 
import re
import sqlite3
import subprocess

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/transcript/<string:video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        logging.info(f"Processing transcript for video ID '{video_id}'.")
        transcript = get_youtube_transcript(video_id)
        channel_name = get_youtube_channel_name(video_id)
        words = [word.lower() for word in re.findall(r'\w+', transcript)]

        # Post or get the channel ID from the external database
        channel_id = post_channel_to_external_db(channel_name)

        word_counts = {}
        futures = []

        # Use ThreadPoolExecutor to post word counts concurrently
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit tasks and keep track of future-to-word mapping
            future_to_word = {executor.submit(post_word_to_external_db, word): word for word in words}

            for future in as_completed(future_to_word):
                word = future_to_word[future]
                try:
                    word, word_id = future.result()
                    if word_id is not None:
                        word_counts[word_id] = word_counts.get(word_id, 0) + 1
                        logging.debug(f"Processed word '{word}' with word_id '{word_id}'.")
                except Exception as e:
                    logging.error(f"Error processing word '{word}': {e}")

        # Post video data to the external database
        post_video_to_external_db(channel_id, video_id, word_counts)

        logging.info(f"Successfully processed transcript for video ID '{video_id}'.")
        return jsonify({"transcript": transcript, "channel_name": channel_name})
    except Exception as e:
        logging.error(f"Failed to process transcript for video ID '{video_id}': {e}")
        return jsonify({"error": str(e)}), 500

# @youtube_bp.route('/channel/<string:channel_name>/transcribe', methods=['GET'])
# def transcribe_channel_videos(channel_name):
#     try:
#         # Find the channel ID using the channel name
#         channel_id = get_channel_id_from_name(channel_name)

#         # Get the recent video IDs for the channel
#         video_ids = get_channel_video_ids(channel_id)

#         # Transcribe each video and store the results
#         transcripts = {}
#         for video_id in video_ids:
#             transcript = get_youtube_transcript(video_id)
#             transcripts[video_id] = transcript

#         return jsonify({"transcripts": transcripts})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500