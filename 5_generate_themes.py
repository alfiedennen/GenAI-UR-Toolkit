import os
import requests
import math

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

def count_tokens(text):
    return len(text.split())

def split_text(text, max_tokens):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if count_tokens(' '.join(current_chunk) + ' ' + word) <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def analyze_transcript(transcript_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    max_tokens = 4096  # Adjust this value based on the model's maximum token limit
    text_chunks = split_text(transcript_text, max_tokens)

    analysis_results = []

    for chunk in text_chunks:
        payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert user researcher analyzing interview text to find common themes. Provide quote-based citations from the transcript to support each theme you identify. Make sure not to miss any subtle themes or insights, we care about even small things."
                },
                {
                    "role": "user",
                    "content": chunk
                }
            ],
            "max_tokens": 500,
            "n": 1,
            "stop": None,
            "temperature": 0.7
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            analysis_results.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while analyzing the transcript chunk.")
            print(f"Error details: {str(e)}")

    return analysis_results

def save_analysis(analysis_results, output_path):
    with open(output_path, 'w') as file:
        for result in analysis_results:
            if result is not None and 'choices' in result and len(result['choices']) > 0:
                analysis_text = result['choices'][0]['message']['content']
                file.write(analysis_text + '\n\n')
            else:
                print("No valid analysis received for a chunk.")

    print(f"Analysis saved to: {output_path}")

if __name__ == '__main__':
    if api_key is None:
        print("Exiting due to missing API key.")
    else:
        transcript_path = "transcript.txt"
        analysis_path = "analysis.txt"

        with open(transcript_path, 'r') as file:
            transcript_text = file.read()

        analysis_results = analyze_transcript(transcript_text)
        save_analysis(analysis_results, analysis_path)