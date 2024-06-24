import librosa

def analyze_audio(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    
    return {
        'tempo': tempo,
        'mfcc': mfcc,
        'chroma': chroma,
        'spectral_contrast': spectral_contrast,
        'tonnetz': tonnetz
    }