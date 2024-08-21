### `README.md`

# YT-Nexus-DB

YT-Nexus-DB is an API designed to provide YouTube video transcript and metadata storage, accessible via the YT Nexus client. 

## Features

- Transcribe YouTube videos and store transcripts in the database.
- Fetch video transcripts and channel information.
- Retrieve top videos and common words from channels.
- Search for videos by keyword.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/KeaganGilmore/yt-nexus-db.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd yt-nexus-db
   ```

3. **Install the dependencies:**

   Ensure you have Python 3.8+ and pip installed. Then run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask server:**

   ```bash
   python app.py
   ```

2. **Access the API endpoints:**

   - **Transcribe a video:**

     ```http
     GET /youtube/transcript/<video_id>
     ```

   - **Transcribe all videos from a channel:**

     ```http
     GET /youtube/channel/<channel_name>/transcribe
     ```

### About Us

Welcome to YT Nexus Python API, a key component of the YT Nexus ecosystem, deployed by LX Library (https://lxlibrary.online).

In response to recent changes in YouTube's regulations that rendered previous YouTube Keyword Search (YTKS) setups ineffective (at the time of writing, changes may occur), we’ve developed the YT Nexus a DB. 

This API is designed to handle video transcriptions and manage metadata efficiently by posting to the yt-nexus db which will be accessible to anyone (largely via the client side), adapting to the new constraints imposed by YouTube.

**Key Features:**
- **Transcribe YouTube Videos:** Retrieve accurate transcripts of YouTube videos using our API.
- **Channel Metadata Management:** Store and access information about YouTube channels and their videos.
- **Community Contributions:** Contribute to a collective effort by running scripts to transcribe videos and enrich our database.

We value community contributions immensely. You can get involved by:

1. **Cloning the Repository:** Access the source code and setup instructions at [YT-Nexus-DB](https://github.com/KeaganGilmore/yt-nexus-db).
2. **Running the API:** Deploy the API on your local environment to start working with video transcriptions and metadata.
3. **Contributing:** Enhance the project by improving scripts or adding new features. Your contributions help us build a more comprehensive tool for the entire community.

Due to the limitations on direct interactions with YouTube for video transcription, the effectiveness of this project relies on collaborative efforts. Your participation is crucial in creating a robust and reliable YouTube keyword search solution.

We appreciate your support in making YT Nexus a valuable resource for everyone!


### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- **Email**: [keagangilmore@gmail.com](mailto:keagangilmore@gmail.com)
- **Discord**: [keagan2980](https://discord.com/users/keagan2980)
```
## Acknowledgments

- Special thanks to all contributors and the open-source community.
- BattlePig, the original creator of ytks.
```

### `pyproject.toml`

### Instructions for `pyproject.toml`

1. **Install Poetry (if not already installed):**

   ```bash
   pip install poetry
   ```

2. **Install dependencies:**

   ```bash
   poetry install
   ```

3. **Run the application:**

   ```bash
   poetry run python app.py
   ```