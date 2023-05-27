"""
The goal of this script is to wrap around a speech-to-text transcription program. This script has two
responsibilities:
1. If the transcription program is not running, start it.
2. If the transcription program is running, send a SIGNAL to the program to tell it to stop recording and start transcription

When the program receives the SIGNAL, it should do the following:
Transcribing the audio consists of the following steps:
1. Write the audio to some file on the system
2. Send the audio via the OpenAI SDK to the Whisper API
3. Receive the transcription from the Whisper API
4. logger the transcription to the keyboard buffer
"""

import os

import os
import signal
import psutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PIDFILE="/tmp/transcribe.pid"

def start_transcription():
    logger.info("Starting transcription")
    os.system("/usr/local/bin/python3 /Users/jhallard/bin/transcribe.py")

def stop_transcription():
    logger.info(f"Process {pid} is running")
    os.kill(pid, signal.SIGUSR1)  # change to whatever signal you want to send


if __name__ == "__main__":
    if os.path.isfile(PIDFILE):
        with open(PIDFILE, 'r') as f:
            pid = int(f.read().strip())
            
        if psutil.pid_exists(pid):
            logger.info(f"Process {pid} is running")
            stop_transcription()
        else:
            start_transcription()
    else:
        start_transcription()
        logger.info(f"{PIDFILE} does not exist")

