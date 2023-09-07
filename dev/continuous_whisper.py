"""
Don't bother with trying to do fancy things to detect the beginning and end of speech. Just let the user
control that with tapping a key. It will be ok. I think a guiding light of this whole thing will be the idea
that we can get humans to adapt to working with LLMs quickly. So let's build some workflows that may involve 
building new muscle memory, but that can make for robust interactions with LLMs. 
"""
import reviver.logger
import openai
from keys import WHISPER_API_KEY
import pyaudio
import wave
from pathlib import Path
from threading import Thread, Event
import time
logger = reviver.logger.get(__name__)

# Substitute 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = WHISPER_API_KEY

# Define some constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  # Change this to the duration you want
WAVE_OUTPUT_FILENAME = "dev/file.wav"

def record_chunk(stop_event:Event, destination_file:Path):
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print('Recording...')
    while not stop_event.is_set():
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print('Finished recording')

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save as a WAV file
    wf = wave.open(str(destination_file), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    logger.info('Done. Your recording is saved as ' + str(destination_file)+ '.')
    stop.clear()

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
if __name__=="__main__":
    from reviver import ROOT

    stop = Event()
    stop.clear() # just to be explicit


    temp_wav = Path(ROOT, "dev", "temp.wav")

    thread = Thread(target=record_chunk, args=[stop, temp_wav], daemon=True)
    thread.start()
    wait = input("Press Enter to Stop")
    stop.set()

    while stop.is_set():
        time.sleep(0.1)
    
    print(transcribe(temp_wav))