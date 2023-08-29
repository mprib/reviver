import pyaudio
import wave

# Define some constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  # Change this to the duration you want
WAVE_OUTPUT_FILENAME = "dev/file.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
frames = []

print('Recording...')

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print('Finished recording')

# Stop recording
stream.stop_stream()
stream.close()
audio.terminate()

# Save as a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print('Done. Your recording is saved as ' + WAVE_OUTPUT_FILENAME + '.')