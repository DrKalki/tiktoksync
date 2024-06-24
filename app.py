import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, session
from urllib.parse import quote as url_quote
from spotipy import oauth2
import spotipy
import youtube_dl

# Load environment variables from .env file
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurations
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Spotify OAuth
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='playlist-read-private')

# Setup logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/tiktoksync.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    app.logger.info('Fetched playlists for user')
    
    return render_template('home.html', playlists=playlists)

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('home'))

@app.route('/fetch_audio', methods=['POST'])
def fetch_audio():
    url = request.form['tiktok_url']
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        app.logger.info(f'Successfully downloaded audio from URL: {url}')
    except Exception as e:
        app.logger.error(f'Error downloading audio from URL: {url}, Error: {e}')
        flash('Failed to download audio. Please check the URL and try again.', 'danger')
        return redirect(url_for('home'))
    
    flash('Audio successfully downloaded and processed.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8888)