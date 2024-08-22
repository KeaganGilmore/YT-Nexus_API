import unittest
from unittest.mock import patch, MagicMock
from youtube.utils import get_youtube_transcript, get_youtube_channel_at_tag

class TestYoutubeUtils(unittest.TestCase):
    @patch('youtube.utils.subprocess.check_output')
    def test_get_youtube_transcript(self, mock_check_output):
        mock_check_output.return_value = '{"events": [{"segs": [{"utf8": "Test transcript"}]}]}'
        result = get_youtube_transcript('test_video_id')
        self.assertEqual(result, 'Test transcript')

    @patch('youtube.utils.subprocess.check_output')
    def test_get_youtube_transcript_error(self, mock_check_output):
        mock_check_output.side_effect = Exception("Test error")
        with self.assertRaises(Exception):
            get_youtube_transcript('test_video_id')

    @patch('youtube.utils.subprocess.check_output')
    def test_get_youtube_channel_at_tag(self, mock_check_output):
        mock_check_output.return_value = '@TestChannel'
        result = get_youtube_channel_at_tag('test_video_id')
        self.assertEqual(result, 'TestChannel')

    @patch('youtube.utils.subprocess.check_output')
    def test_get_youtube_channel_at_tag_error(self, mock_check_output):
        mock_check_output.side_effect = Exception("Test error")
        with self.assertRaises(Exception):
            get_youtube_channel_at_tag('test_video_id')

if __name__ == '__main__':
    unittest.main()