import cv2
import os
from pytube import YouTube

def download_video(url, output_path):
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    stream.download(output_path=output_path, filename="video.mp4")

def extract_frames(video_path, output_folder, fps=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    frame_count = 0
    success, image = video.read()
    while success:
        if frame_count % int(video.get(cv2.CAP_PROP_FPS) / fps) == 0:
            timestamp = int(video.get(cv2.CAP_PROP_POS_MSEC))
            filename = f"{timestamp}.jpg"
            cv2.imwrite(os.path.join(output_folder, filename), image)
        success, image = video.read()
        frame_count += 1

if __name__ == '__main__':
    video_url = "https://www.youtube.com/watch?v=E0fB9_V4TUU&list=PLJYAzgI3UdEolIrrXUK8qu2pPrfFmDWzJ&ab_channel=SofiaValdes"
    video_path = "video.mp4"
    frames_folder = "frames"

    download_video(video_url, ".")
    extract_frames(video_path, frames_folder)