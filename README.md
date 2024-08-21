# YT Nexus

YT Nexus is a Flask API for accessing YouTube video transcripts, channel information, and related data. It provides endpoints to retrieve video transcripts, find common words, get top videos, and more.

## Prerequisites

- Python 3.x
- Flask
- SQLite
- `yt-dlp` (YouTube video downloader)
- `scrapetube` (YouTube scraper)
- `youtubesearchpython` (YouTube search API)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/KeaganGilmore/YT-Nexus_API.git
    cd YT-Nexus_API
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install `yt-dlp`**:
    ```bash
    pip install yt-dlp
    ```

4. **Install `scrapetube`**:
    ```bash
    pip install scrapetube
    ```

5. **Install `youtubesearchpython`**:
    ```bash
    pip install youtubesearchpython
    ```

## Usage

1. **Set up the database**:
    Run the Flask application to initialize the SQLite database:
    ```bash
    python app.py
    ```

2. **Start the Flask application**:
    ```bash
    python app.py
    ```

3. **Access the API endpoints**:

    - **Get Transcript of a Video**:
      ```
      GET /youtube/transcript/<video_id>
      ```
      - Returns the transcript and channel name for the specified video ID.

    - **Get Video Transcript**:
      ```
      GET /youtube/video/<video_id>
      ```
      - Returns the transcript for the specified video ID.

    - **Get Common Words for a Channel**:
      ```
      GET /youtube/channel/<channel_name>/common-words
      ```
      - Returns the most common words used in videos of the specified channel.

    - **Get Top Videos for a Channel**:
      ```
      GET /youtube/channel/<channel_name>/top-videos
      ```
      - Returns the top videos for the specified channel based on word count.

    - **Get Videos with a Specific Keyword**:
      ```
      GET /youtube/channel/<channel_name>/keyword/<keyword>
      ```
      - Returns a list of videos containing the specified keyword in the specified channel.

    - **Transcribe All Videos in a Channel**:
      ```
      GET /youtube/channel/<channel_name>/transcribe
      ```
      - Returns transcripts for all videos in the specified channel.

## Code Structure

- **`app.py`**: Main Flask application entry point.
- **`youtube/views.py`**: Contains route definitions for YouTube-related endpoints.
- **`database.py`**: Contains database schema creation and helper functions for interacting with the SQLite database.
- **`utils.py`**: Contains utility functions for interacting with YouTube (e.g., fetching transcripts, channel info).

## Error Handling

The API returns standard HTTP status codes:
- `200 OK` for successful requests.
- `500 Internal Server Error` for server-side issues (e.g., failed to fetch transcript).

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. For any questions or issues, please contact Keagan Gilmore at keagangilmore@gmail.com.
