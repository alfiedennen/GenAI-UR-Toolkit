import os
import requests

def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("API key file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the API key: {e}")
        return None

api_key = read_api_key("key.txt")

def transcribe_audio(audio_path, output_path):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    with open(audio_path, "rb") as audio_file:
        files = {
            "file": audio_file,
            "model": (None, "whisper-1"),
            "response_format": (None, "text")
        }
        response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files)
    
    with open(output_path, "w") as output_file:
        output_file.write(response.text)

if __name__ == '__main__':
    if api_key is None:
        print("Exiting due to missing API key.")
    else:
        audio_path = "D:\\Visual Studio Code Projects\\Batch OCR\\audio copy.mp3"
        transcript_path = "transcript.txt"

        transcribe_audio(audio_path, transcript_path)