from spotipy.oauth2 import SpotifyOAuth
from config import Config
from flask import session, redirect, url_for
import spotipy
import time

class SpotifyAuth:
    def __init__(self):
        self.sp_oauth = SpotifyOAuth(client_id=Config.SPOTIPY_CLIENT_ID,
                                     client_secret=Config.SPOTIPY_CLIENT_SECRET,
                                     redirect_uri=Config.SPOTIPY_REDIRECT_URI,
                                     scope='user-library-read')

    def get_spotify_token(self):
        token_info = session.get('token_info', None)
        if not token_info:
            return redirect(url_for('login'))

        now = int(time.time())
        is_token_expired = token_info['expires_at'] - now < 60

        if is_token_expired:
            token_info = self.sp_oauth.refresh_access_token(token_info['refresh_token'])

        return token_info

    def get_spotify_client(self, token_info):
        return spotipy.Spotify(auth=token_info['access_token'])

spotify_auth = SpotifyAuth()