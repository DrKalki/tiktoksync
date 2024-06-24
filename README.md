# TikTok Sync

This project syncs TikTok audio with Spotify songs, matching the TikTok audio with similar tracks from a Spotify playlist.

## Features

- Authenticate with Spotify
- Analyze TikTok audio files
- Fetch TikTok audio from a URL
- Match TikTok audio with songs from Spotify playlists
- Display matched song information

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/DrKalki/tiktoksync.git
    cd tiktoksync
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    pip install -r requirements.txt
    ```

3. Create a `.env` file with your Spotify API credentials:

    ```plaintext
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Open your browser and go to `http://localhost:8888`.

## Usage

1. Authenticate with your Spotify account.
2. Upload a TikTok audio file or enter a TikTok URL.
3. The application will analyze the audio and match it with a similar song from your Spotify playlists.
4. The matched song will be displayed with its information and a preview.

## License

MIT License