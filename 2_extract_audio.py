from pytube import YouTube

def download_audio(video_url, output_path):
    video = YouTube(video_url)
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=output_path, filename="audio.mp3")

if __name__ == '__main__':
    video_url = "https://www.youtube.com/watch?v=E0fB9_V4TUU&list=PLJYAzgI3UdEolIrrXUK8qu2pPrfFmDWzJ"
    audio_path = "audio.mp3"

    download_audio(video_url, audio_path)