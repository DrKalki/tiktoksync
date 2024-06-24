from moviepy.editor import VideoFileClip, AudioFileClip

def replace_audio(video_file_path, audio_file_path):
    video = VideoFileClip(video_file_path)
    audio = AudioFileClip(audio_file_path)
    video = video.set_audio(audio)
    output_path = 'output_video.mp4'
    video.write_videofile(output_path)
    return output_path