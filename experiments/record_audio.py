import pyaudio
import time
import argparse
import wave
import os

# Settings for the audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
audio = pyaudio.PyAudio()
frames = []
recording = False

# Initialize PyAudio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

def record(duration: float, output_filename: str):
    print("Recording...")
    start = time.time()

    while time.time() - start < duration:
        data = stream.read(CHUNK)
        frames.append(data)

    print(f"Finished recording {duration} seconds")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save audio file
    waveFile = wave.open(output_filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    os._exit(0)  # Exit the script


def parse_args():
    parser = argparse.ArgumentParser(description='Record audio')
    parser.add_argument('--duration', type=int, default=5,
                        help='Duration of the recording in seconds')
    parser.add_argument('--output', type=str, default='output.wav',
                        help='Name of the output file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # Start recording
    record(args.duration, args.output)

