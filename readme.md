# User Research Toolkit README

## Overview

The User Research Toolkit is designed to assist user researchers in reducing the time it takes to synthesise research findings. It includes functionalities for downloading videos and audio from YouTube, extracting frames from videos, transcribing audio content, and extracting and analyzing text from images or transcriptions. This toolkit aims to streamline the data collection and analysis phases of user research.

## Features

- **Video and Audio Download**: Download videos and their audio tracks directly from YouTube URLs.
- **Frame Extraction**: Extract specific frames from videos, allowing for detailed analysis of visual content.
- **Audio Transcription**: Convert audio content into text, facilitating content analysis and theme identification.
- **Text Extraction from Images**: Extract readable text from images, useful for analyzing visual data like post-its or signage.
- **Text Analysis**: Analyze text to identify common themes, insights, and patterns.

## Installation

Before using the toolkit, ensure you have Python installed on your system. Additionally, you'll need to install the following Python libraries:

```bash
pip install cv2 pytube requests
```

## Usage

### Downloading Video/Audio from YouTube

```python
from pytube import YouTube

def download_video(url, output_path):
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    stream.download(output_path=output_path)

def download_audio(video_url, output_path):
    video = YouTube(video_url)
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=output_path)
```

### Extracting Frames from Videos

```python
import cv2
import os

def extract_frames(video_path, output_folder, fps=1):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extract frames
    # ...
```

### Transcribing Audio

```python
import requests

def transcribe_audio(audio_path, output_path, api_key):
    # Transcribe audio
    # ...
```

### Extracting and Analyzing Text

Text can be extracted from images using the GPT-4 Vision model, and transcripts can be analyzed for themes and insights using GPT-4.

```python
import requests

def extract_text_gpt4(image_path, api_key):
    # Extract text from images
    # ...

def analyze_transcript(transcript_text, api_key):
    # Analyze text for themes
    # ...
```

## Configuration

Most scripts require an API key for functionality such as transcribing audio or extracting text from images. Ensure you have the necessary API keys and have them stored in a file named `key.txt`.

## Contributing

Contributions to the toolkit are welcome. Please ensure to follow the project's coding standards and submit pull requests for any enhancements, bug fixes, or feature additions.

## License

This toolkit is released under the MIT License. See the `LICENSE` file for more details.