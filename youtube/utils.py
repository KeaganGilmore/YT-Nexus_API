import subprocess
import logging
import os
import json

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

def get_youtube_channel_at_tag(video_id):
    try:
        command = [
            'yt-dlp',
            '--skip-download',
            '--no-warnings',
            '--no-simulate',
            '--get-filename',
            '--output', '%(uploader_id)s',
            f'https://www.youtube.com/watch?v={video_id}'
        ]
        output = subprocess.check_output(command, universal_newlines=True)
        handle = output.strip()
        
        # Remove the '@' symbol if it is present
        if handle.startswith('@'):
            handle = handle[1:]
        
        return handle
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get channel @ tag for video {video_id}: {e}")
        return "Error: Failed to get channel @ tag."
    except Exception as e:
        logging.error(f"An error occurred while getting channel @ tag for video {video_id}: {e}")
        return f"An error occurred: {str(e)}"
    
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

