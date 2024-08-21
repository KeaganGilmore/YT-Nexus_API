from flask import Blueprint, jsonify, request
from utils import * 
from database import get_or_create_word, get_or_create_channel, insert_video, get_common_words, get_top_videos
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

        # Get or create the channel
        channel_id = get_or_create_channel(channel_name)

        # Create a dictionary of word counts
        word_counts = {}
        for word in words:
            word_id = get_or_create_word(word)
            word_counts[word_id] = word_counts.get(word_id, 0) + 1

        # Insert video data into the database
        insert_video(channel_id, video_id, word_counts)

        return jsonify({"transcript": transcript, "channel_name": channel_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@youtube_bp.route('/video/<string:video_id>', methods=['GET'])
def get_video_transcript(video_id):
    try:
        transcript = get_youtube_transcript(video_id)
        return jsonify({"transcript": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@youtube_bp.route('/channel/<string:channel_name>/common-words', methods=['GET'])
def get_channel_common_words(channel_name):
    try:
        channel_id = get_or_create_channel(channel_name)
        common_words = get_common_words(channel_id)
        return jsonify({"common_words": common_words})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@youtube_bp.route('/channel/<string:channel_name>/top-videos', methods=['GET'])
def get_channel_top_videos(channel_name):
    try:
        channel_id = get_or_create_channel(channel_name)
        top_videos = get_top_videos(channel_id)
        return jsonify({"top_videos": top_videos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@youtube_bp.route('/channel/<channel_name>/keyword/<keyword>', methods=['GET'])
def get_videos_with_keyword(channel_name, keyword):
    try:
        channel_id = get_or_create_channel(channel_name)
        conn = sqlite3.connect('api.db')
        c = conn.cursor()

        c.execute('''
            SELECT vd.video_id, wc.count
            FROM video_details vd
            JOIN word_counts wc ON vd.id = wc.video_id
            JOIN dictionary d ON wc.word_id = d.id
            WHERE vd.channel_id = ? AND d.word = ?
            ORDER BY wc.count DESC;
        ''', (channel_id, keyword.lower()))

        videos = [{'video_id': row[0], 'count': row[1]} for row in c.fetchall()]
        conn.close()
        return jsonify({"videos": videos})
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