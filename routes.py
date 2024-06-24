from flask import Flask, request, redirect, url_for, flash, session
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Blueprint, render_template

# Create a blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return redirect(url_for('home'))

@routes.route('/home')
def home():
    playlists = []  # Example data; replace with actual data fetching logic
    return render_template('home.html', playlists=playlists)

@routes.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                            scope="playlist-read-private")
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@routes.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                            scope="playlist-read-private")
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    app.logger.debug(f"Received token info: {token_info}")
    session['token_info'] = token_info
    return redirect(url_for('home'))

@routes.route('/analyze', methods=['POST'])
def analyze():
    app.logger.debug("Analyzing uploaded audio")
    audio_file = request.files['audio']
    if not audio_file:
        flash("No audio file uploaded")
        return redirect(url_for('home'))

    audio_file_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(audio_file_path)
    app.logger.debug(f"Saved audio file to {audio_file_path}")

    try:
        tiktok_audio_features = analyze_audio(audio_file_path)
        app.logger.debug(f"Analyzed audio features: {tiktok_audio_features}")
    except Exception as e:
        app.logger.error(f"Error analyzing audio: {e}")
        flash("Failed to analyze audio. Please check the file and try again.", 'danger')
        return redirect(url_for('home'))

    flash("Audio successfully uploaded and processed.", 'success')
    return redirect(url_for('home'))

def analyze_audio(file_path):
    # Dummy function; replace with actual audio analysis logic
    return {"feature1": "value1", "feature2": "value2"}

# Register blueprint in the main app
def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8888)