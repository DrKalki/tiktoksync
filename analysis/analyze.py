import librosa

def analyze_audio(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    return {'tempo': tempo, 'mfcc': mfcc}