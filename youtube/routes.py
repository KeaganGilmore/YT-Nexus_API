from flask import Blueprint, jsonify, request
from services import *
import scrapetube
youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/transcript/<string:video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        update_cache_from_external()
        result = process_video(video_id)
        return jsonify({"status": "Video processed successfully", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@youtube_bp.route('/start-processing', methods=['POST'])
def start_processing():
    update_cache_from_external()
    continuously_process_videos()
    return jsonify({"status": "Video processing already running"}), 202

# Endpoint to scrape and process videos from a YouTube channel
@youtube_bp.route('/scrape-and-process', methods=['POST'])
def scrape_and_process():
    # Get the YouTube channel ID from the request body
    data = request.get_json()
    channel_id = data.get('channel_id')

    if not channel_id:
        return jsonify({'error': 'No channel_id provided'}), 400

    try:
        # Scrape all video IDs from the channel
        videos = scrapetube.get_channel(channel_id)
        video_ids = [video['videoId'] for video in videos]

        # Process each video using the process_videos endpoint
        process_url = "http://your-process-videos-endpoint-url"  # Replace with your actual endpoint URL
        results = []

        for video_id in video_ids:
            response = requests.post(process_url, json={'video_id': video_id})
            results.append(response.json())

        return jsonify({'success': True, 'results': results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


### TEMPREMENTAL MAY NOT WORK
@youtube_bp.route('/process-channel/<string:channel_name>', methods=['POST'])
def process_channel(channel_name):
    logging.info(f"Received request to process channel: {channel_name}")
    try:
        update_cache_from_external()
        results = process_channel_videos(channel_name)
        return jsonify({"status": "Channel processed successfully", "results": results})
    except Exception as e:
        logging.error(f"Error in process_channel route: {str(e)}")
        return jsonify({"error": str(e)}), 500