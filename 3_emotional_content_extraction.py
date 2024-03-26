import os
import base64
import requests

# Function to read API key from a file
def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()  # Read the first line and remove any trailing newline characters
    except FileNotFoundError:
        print("API key file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the API key: {e}")
        return None

# Replace the direct api_key assignment with a call to read it from key.txt
api_key = read_api_key("key.txt")  # Ensure this path is correct relative to your script's execution directory

# Folder containing images - adjust to your images' directory
image_folder = 'frames'

def extract_text_gpt4(image_path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
   
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": "determine what the emotional state of the face on the left in this image is. Be sparing in description, for example: pleased. or, surprised. Or, puzzled, etc."
            },
            {
                "role": "system",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
   
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while processing image: {image_path}")
        print(f"Error details: {str(e)}")
        return None

def process_images(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    output_folder = "responses"  # Folder to save the response text files
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            response = extract_text_gpt4(file_path)
            
            if response is not None and 'choices' in response and len(response['choices']) > 0:
                extracted_text = response['choices'][0]['message']['content']
                
                # Save the response as a text file
                output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_response.txt")
                with open(output_file, "w") as file:
                    file.write(extracted_text)
                
                print(f"Response saved for file: {filename}")
                print(f"Extracted text:\n{extracted_text}\n")
            else:
                print(f"No valid response received for file: {filename}")

if __name__ == '__main__':
    if api_key is None:
        print("Exiting due to missing API key.")
    else:
        process_images(image_folder)