import numpy as np

def find_best_match(tiktok_audio_features, spotify_audio_features):
    best_match = None
    smallest_difference = float('inf')
    
    for spotify_features in spotify_audio_features:
        if spotify_features is None:
            continue
        
        # Calculate feature differences
        tempo_diff = abs(tiktok_audio_features['tempo'] - spotify_features['tempo'])
        mfcc_diff = np.linalg.norm(tiktok_audio_features['mfcc'] - spotify_features['mfcc'])
        chroma_diff = np.linalg.norm(tiktok_audio_features['chroma'] - spotify_features['chroma'])
        spectral_contrast_diff = np.linalg.norm(tiktok_audio_features['spectral_contrast'] - spotify_features['spectral_contrast'])
        tonnetz_diff = np.linalg.norm(tiktok_audio_features['tonnetz'] - spotify_features['tonnetz'])
        
        # Combine differences (weighting can be adjusted)
        total_diff = (tempo_diff * 0.2 + mfcc_diff * 0.2 + chroma_diff * 0.2 +
                      spectral_contrast_diff * 0.2 + tonnetz_diff * 0.2)
        
        if total_diff < smallest_difference:
            smallest_difference = total_diff
            best_match = spotify_features
    
    return best_match