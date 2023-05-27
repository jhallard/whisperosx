import pyaudio
import wave
import signal
import os

# Settings for the audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "file.wav"
audio = pyaudio.PyAudio()
frames = []
recording = False

# Initialize PyAudio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

def record():
    global recording
    recording = True
    print("Recording...")
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

def stop_recording(signum, frame):
    global recording
    print("Finished recording")
    recording = False

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save audio file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    os._exit(0)  # Exit the script

# Register the signal handler
signal.signal(signal.SIGUSR1, stop_recording)

# Start recording
record()

