import openai
import base64
from keys import WHISPER_API_KEY

# Substitute 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = WHISPER_API_KEY

def transcribe(file_path):
    with open(file_path, "rb") as f:
        transcript = openai.Audio.transcribe(
        file = f,
        model = "whisper-1",
        response_format="text",
        language="en"
    )   

    print(transcript)
# Substitute 'file.wav' with your actual .wav file path
file_path = 'dev/file.wav'
print(transcribe(file_path))