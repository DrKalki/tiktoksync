from flask import Flask, render_template, request, redirect, url_for, flash, session
from spotipy import oauth2, Spotify
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Set up logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/tiktoksync.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    playlists = []  # Example data; replace with actual data fetching logic
    return render_template('home.html', playlists=playlists)

@app.route('/login')
def login():
    # Your login logic here
    return render_template('login.html')

@app.route('/callback')
def callback():
    # Your callback logic here
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8888)