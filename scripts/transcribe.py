import pyaudio
import openai
import time
import wave
import signal
import sys
import os
import threading
import argparse
import pyautogui
import tempfile
import logging

from typing import Optional, Callable
from functools import partial


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stop_recording_event = threading.Event()

# Settings for the audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
audio = pyaudio.PyAudio()
frames = []

before = time.time()
# Initialize PyAudio
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

logger.info(f"Took {time.time() - before:.4f} seconds to initialize PyAudio")

def make_sound() -> None:
    # https://stackoverflow.com/questions/13941/python-sound-bell
    sys.stdout.write('\a')
    sys.stdout.flush()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Record audio')
    parser.add_argument('--max-duration', type=int, default=30,
                        help='Maximum duration of the recording in seconds')
    parser.add_argument('--output', type=str, default=None,
                        help='Name of the output file (tempfile is used if not specified)')
    parser.add_argument('--prompt', type=str, default=None,
                        help='Prompt to use for the transcription')
    return parser.parse_args()


def record():
    make_sound()
    stop_recording_event.set()
    logger.info("Recording...")
    last = time.time()
    while stop_recording_event.is_set():
        if time.time() - last > 1:
            logger.info("Still Recording...")
            last = time.time()
        data = stream.read(CHUNK)
        frames.append(data)
        time.sleep(0.01)

    logger.info(f"Finished recording loop")

def stop_recording(signum=None, frame=None, output_filename: Optional[str] = None):

    if not output_filename:
        raise ValueError("output_filename must be specified")
    global stop_recording_event
    if not stop_recording_event.is_set():
        # Already been stopped by signal handler or thread
        return

    make_sound()
    logger.info("Finished recording, processing stream..")
    try:
        stop_recording_event.clear()

        # Stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        logger.info(f"Writing stream to {output_filename}..")

        # Save audio file
        waveFile = wave.open(output_filename, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
    except Exception as e:
        logger.error(f"Error while writing to {output_filename}: {e}", exc_info=True)


def transcribe(input_filename: str, prompt: Optional[str] = None) -> str:
    logger.info(f"Transcribing {input_filename}..")
    audio_file= open(input_filename, "rb")
    before = time.time()
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt=prompt)
    logger.info(f"Transcript from OpenAI (took {time.time() - before:.4f}s): {transcript}")
    return transcript["text"]

def output_transcript(transcript: str) -> None:
    pyautogui.typewrite(transcript)

def register_signal_handler(signal_handler: Callable) -> None:
    # Register the signal handler
    print(f"Registering signal handler for SIGUSR1")
    signal.signal(signal.SIGUSR1, signal_handler)


def write_pid() -> None:
    pid = os.getpid()
    with open("/tmp/transcribe.pid", "w") as f:
        f.write(str(pid))

def clean_pid() -> None:
    try:
        os.remove("/tmp/transcribe.pid")
    except FileNotFoundError:
        pass

def run(max_duration: float, output_filename: Optional[str] = None) -> str:
    # Start recording in a new thread

    # If the output_filename is not specified, use a temporary output_filename
    if output_filename is None:
        output_filename = tempfile.mktemp(suffix='.wav')

    logger.info(f"Recording for {max_duration}s to {output_filename}")

    handler = partial(stop_recording, output_filename=output_filename)
    register_signal_handler(handler)

    recording_thread = threading.Thread(target=record)
    recording_thread.daemon = True
    recording_thread.start()

    # Start a timer, when the timer ends, stop the recording
    timer = threading.Timer(max_duration, handler)
    timer.daemon = True
    timer.start()

    recording_thread.join(timeout=max_duration)

    # We have to wait for the `stop_recording` method to finish flushing the file
    start, last = time.time(), time.time()
    while not os.path.exists(output_filename) and time.time() - start < 5:
        if time.time() - last > 0.5:
            logger.info(f"Waiting for {output_filename} to be written")
            last = time.time()
        time.sleep(0.1)

    if not os.path.exists(output_filename):
        logger.error(f"Expected audio file {output_filename} to be written, but it was not")
        return

    # We now have the recording written to the output_file, time to transcribe it
    text = transcribe(output_filename)

    # Clean up after ourselves
    os.remove(output_filename)

    # And tell the desktop to output the text via keystrokes
    output_transcript(text)


if __name__ == "__main__":
    args = parse_args()
    write_pid()
    try:
        run(args.max_duration, args.output)
    finally:
        clean_pid()
    os._exit(0)  # Exit the script
