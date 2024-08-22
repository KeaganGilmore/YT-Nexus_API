import unittest
from unittest.mock import patch, MagicMock
from services.video_processing import process_video, continuously_process_videos

class TestVideoProcessing(unittest.TestCase):
    @patch('services.video_processing.get_youtube_transcript')
    @patch('services.video_processing.get_youtube_channel_at_tag')
    @patch('services.video_processing.post_new_words')
    @patch('services.video_processing.update_cache')
    def test_process_video(self, mock_update_cache, mock_post_new_words, mock_get_channel, mock_get_transcript):
        mock_get_transcript.return_value = "This is a test transcript"
        mock_get_channel.return_value = "TestChannel"
        mock_post_new_words.return_value = None
        mock_update_cache.return_value = None

        result = process_video('test_video_id')
        
        self.assertIn('transcript', result)
        self.assertIn('channel_name', result)
        self.assertEqual(result['channel_name'], "TestChannel")

    @patch('services.video_processing.get_youtube_transcript')
    def test_process_video_error(self, mock_get_transcript):
        mock_get_transcript.side_effect = Exception("Test error")
        with self.assertRaises(Exception):
            process_video('test_video_id')

    @patch('services.video_processing.process_video')
    @patch('services.video_processing.fetch_random_youtube_video_ids')
    def test_continuously_process_videos(self, mock_fetch_ids, mock_process_video):
        mock_fetch_ids.return_value = ['test_video_id']
        mock_process_video.return_value = None

        # We'll run the function once and then break the loop
        def side_effect():
            continuously_process_videos()
            raise KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            side_effect()

        mock_process_video.assert_called_once_with('test_video_id')

if __name__ == '__main__':
    unittest.main()