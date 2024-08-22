# YT-Nexus-DB

YT-Nexus-DB is an API designed to facilitate the storage and retrieval of YouTube video transcripts and metadata. It serves as a backbone for the YT Nexus client, enabling users to transcribe videos, analyze channel data, and perform keyword searches across a vast library of YouTube content.

## Features

- **Video Transcription:** Transcribe YouTube videos and store their transcripts in a structured database.
- **Metadata Management:** Fetch and store detailed video metadata, including channel information.
- **Keyword Search:** Perform keyword searches to find relevant videos across stored transcripts.
- **Channel Analytics:** Retrieve top videos and common words from specific channels, helping to uncover trends and patterns.

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

   See pyprojects.toml for dependencies


## Usage

1. **Start the Flask server:**

   ```bash
   python app.py
   ```

2. **Access the API endpoints:**

   - **Transcribe a specific video:**

     ```http
     GET /youtube/transcript/<video_id>
     ```

   - **Transcribe all videos from a channel:**

     ```http
     GET /youtube/channel/<channel_name>/transcribe
     ```

   - **Search for videos by keyword:**

     ```http
     GET /youtube/search/<keyword>
     ```

   - **Fetch channel metadata:**

     ```http
     GET /youtube/channel/<channel_name>/metadata
     ```

   - **Retrieve top videos from a channel:**

     ```http
     GET /youtube/channel/<channel_name>/top_videos
     ```

   - **Get common words used in a channel's videos:**

     ```http
     GET /youtube/channel/<channel_name>/common_words
     ```

## About Us

Welcome to YT Nexus Python API, an essential component of the YT Nexus ecosystem, deployed by [LX Library](https://lxlibrary.online).

**Recent Changes:**
- Due to YouTube's updated policies, traditional methods for keyword searches have become less effective. YT Nexus-DB is our response, focusing on transcript and metadata storage to support robust content analysis and keyword discovery.

**Community Contributions:**
- **Get Involved:** We highly encourage contributions from the community. Whether it's enhancing scripts, adding features, or improving documentation, your involvement makes YT Nexus-DB a better tool for everyone.

**Key Objectives:**
- **Collaborative Effort:** The effectiveness of YT Nexus-DB is amplified by community support. Together, we can build a comprehensive database that adapts to YouTube's evolving ecosystem.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- **Email:** [keagangilmore@gmail.com](mailto:keagangilmore@gmail.com)
- **Discord:** [keagan2980](https://discord.com/users/keagan2980)

## Acknowledgments

- **Contributors:** Special thanks to all contributors and the open-source community.
- **YTKS Inspiration:** BattlePig, the original creator of YTKS, for laying the groundwork.
- **Deployment Support:** Dwidge [@dwidge](https://github.com/dwidge) for assisting in the deployment of YT Nexus DB.

## Note

The current server hosting YT Nexus-DB is not optimized for large-scale data scraping, which limits its efficiency. Community funding would greatly enhance our ability to handle the data volume and improve system performance. Your support is crucial in scaling this project to meet its full potential.
