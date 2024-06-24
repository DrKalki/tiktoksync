from flask import render_template, redirect, url_for, session, request, flash
import logging
from auth.spotify_auth import spotify_auth
from analysis.analyze import analyze_audio
from analysis.match import find_best_match
import youtube_dl

def register_routes(app):
    @app.route('/')
    def login():
        app.logger.debug("Redirecting to Spotify login")
        return redirect(spotify_auth.sp_oauth.get_authorize_url())

    @app.route('/callback')
    def callback():
        app.logger.debug("Handling callback from Spotify")
        token_info = spotify_auth.sp_oauth.get_access_token(request.args['code'])
        app.logger.debug(f"Received token_info: {token_info}")
        session['token_info'] = token_info
        return redirect(url_for('home'))

    @app.route('/home')
    def home():
        app.logger.debug("Loading home page")
        token_info = spotify_auth.get_spotify_token()
        if not token_info:
            flash('Error fetching Spotify token')
            return redirect(url_for('login'))
        
        sp = spotify_auth.get_spotify_client(token_info)
        try:
            playlists = sp.current_user_playlists()
        except spotipy.exceptions.SpotifyException as e:
            app.logger.error(f"Spotify API error: {e}")
            flash('Error fetching playlists from Spotify')
            return redirect(url_for('login'))
        
        app.logger.debug(f"Playlists: {playlists}")
        return render_template('home.html', playlists=playlists['items'])

    @app.route('/analyze', methods=['POST'])
    def analyze():
        app.logger.debug("Analyzing uploaded audio")
        audio_file = request.files['audio']
        if not audio_file:
            flash('No audio file uploaded')
            return redirect(url_for('home'))
        
        audio_file_path = os.path.join('uploads', audio_file.filename)
        audio_file.save(audio_file_path)
        app.logger.debug(f"Saved audio file to {audio_file_path}")

        try:
            tiktok_audio_features = analyze_audio(audio_file_path)
            app.logger.debug(f"Analyzed audio features: {tiktok_audio_features}")
        except Exception as e:
            app.logger.error(f"Error analyzing audio: {e}")
            flash('Error analyzing audio file')
            return redirect(url_for('home'))

        token_info = spotify_auth.get_spotify_token()
        if not token_info:
            flash('Error fetching Spotify token')
            return redirect(url_for('login'))
        
        sp = spotify_auth.get_spotify_client(token_info)
        matched_song = None
        
        try:
            playlists = sp.current_user_playlists()
            for playlist in playlists['items']:
                tracks = sp.playlist_tracks(playlist['id'])['items']
                track_ids = [track['track']['id'] for track in tracks]
                spotify_audio_features = sp.audio_features(track_ids)
                matched_song = find_best_match(tiktok_audio_features, spotify_audio_features)
                if matched_song:
                    break
        except spotipy.exceptions.SpotifyException as e:
            app.logger.error(f"Spotify API error: {e}")
            flash('Error fetching audio features from Spotify')
            return redirect(url_for('home'))
        
        app.logger.debug(f"Matched song: {matched_song}")
        return render_template('matched_song.html', song=matched_song)

    @app.route('/fetch_audio', methods=['POST'])
    def fetch_audio():
        tiktok_url = request.form['tiktok_url']
        if not tiktok_url:
            flash('No TikTok URL provided')
            return redirect(url_for('home'))

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(tiktok_url, download=True)
                audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
                app.logger.debug(f"Downloaded audio file to {audio_file_path}")

            tiktok_audio_features = analyze_audio(audio_file_path)
            app.logger.debug(f"Analyzed audio features: {tiktok_audio_features}")
        except Exception as e:
            app.logger.error(f"Error fetching or analyzing TikTok audio: {e}")
            flash('Error fetching or analyzing TikTok audio')
            return redirect(url_for('home'))

        token_info = spotify_auth.get_spotify_token()
        if not token_info:
            flash('Error fetching Spotify token')
            return redirect(url_for('login'))
        
        sp = spotify_auth.get_spotify_client(token_info)
        matched_song = None
        
        try:
            playlists = sp.current_user_playlists()
            for playlist in playlists['items']:
                tracks = sp.playlist_tracks(playlist['id'])['items']
                track_ids = [track['track']['id'] for track in tracks]
                spotify_audio_features = sp.audio_features(track_ids)
                matched_song = find_best_match(tiktok_audio_features, spotify_audio_features)
                if matched_song:
                    break
        except spotipy.exceptions.SpotifyException as e:
            app.logger.error(f"Spotify API error: {e}")
            flash('Error fetching audio features from Spotify')
            return redirect(url_for('home'))
        
        app.logger.debug(f"Matched song: {matched_song}")
        return render_template('matched_song.html', song=matched_song)