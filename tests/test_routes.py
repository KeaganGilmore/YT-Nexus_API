import unittest
from flask import Flask
from youtube.routes import youtube_bp
from unittest.mock import patch

class TestYoutubeRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(youtube_bp, url_prefix='/youtube')
        self.client = self.app.test_client()

    @patch('youtube.routes.process_video')
    def test_get_transcript(self, mock_process_video):
        mock_process_video.return_value = {"transcript": "Test transcript", "channel_name": "Test Channel"}
        response = self.client.get('/youtube/transcript/test_video_id')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Video processed successfully', response.json['status'])
        self.assertIn('transcript', response.json['result'])

    @patch('youtube.routes.process_video')
    def test_get_transcript_error(self, mock_process_video):
        mock_process_video.side_effect = Exception("Test error")
        response = self.client.get('/youtube/transcript/test_video_id')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

    def test_start_processing(self):
        response = self.client.post('/youtube/start-processing')
        self.assertEqual(response.status_code, 202)
        self.assertIn('Video processing already running', response.json['status'])

if __name__ == '__main__':
    unittest.main()
