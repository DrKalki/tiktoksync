from flask import Flask, redirect, url_for, session, request, render_template
import os
from dotenv import load_dotenv
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth.spotify_auth import spotify_auth
from analysis.analyze import analyze_audio
from analysis.match import find_best_match

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def login():
    logging.debug("Redirecting to Spotify login")
    return redirect(spotify_auth.sp_oauth.get_authorize_url())

@app.route('/callback')
def callback():
    logging.debug("Handling callback from Spotify")
    token_info = spotify_auth.sp_oauth.get_access_token(request.args['code'])
    logging.debug(f"Received token_info: {token_info}")
    session['token_info'] = token_info
    return redirect(url_for('home'))

@app.route('/home')
def home():
    logging.debug("Loading home page")
    token_info = spotify_auth.get_spotify_token()
    sp = spotify_auth.get_spotify_client(token_info)
    playlists = sp.current_user_playlists()
    logging.debug(f"Playlists: {playlists}")
    return render_template('home.html', playlists=playlists)

@app.route('/analyze', methods=['POST'])
def analyze():
    logging.debug("Analyzing uploaded audio")
    audio_file = request.files['audio']
    audio_file_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(audio_file_path)
    logging.debug(f"Saved audio file to {audio_file_path}")

    tiktok_audio_features = analyze_audio(audio_file_path)
    logging.debug(f"Analyzed audio features: {tiktok_audio_features}")

    token_info = spotify_auth.get_spotify_token()
    sp = spotify_auth.get_spotify_client(token_info)
    playlists = sp.current_user_playlists()
    if playlists['items']:
        playlist_id = playlists['items'][0]['id']
        tracks = sp.playlist_tracks(playlist_id)['items']
        track_ids = [track['track']['id'] for track in tracks]
        spotify_audio_features = sp.audio_features(track_ids)
        logging.debug(f"Spotify audio features: {spotify_audio_features}")
    
    matched_song = find_best_match(tiktok_audio_features, spotify_audio_features)
    logging.debug(f"Matched song: {matched_song}")
    return f"Matched Song: {matched_song['name']}"

if __name__ == '__main__':
    app.run(debug=True, port=8888)