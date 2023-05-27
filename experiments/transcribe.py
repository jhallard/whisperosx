from typing import Optional

import argparse
import openai

def parse_args():
    parser = argparse.ArgumentParser(description='Transcribe audio')
    parser.add_argument('--input_filename', type=str, default='output.wav',
                        help='Name of the input file')
    parser.add_argument('--prompt', type=str, default=None,
                        help='Prompt to use for the transcription')
    return parser.parse_args()

def transcribe(input_filename: str, prompt: Optional[str] = None) -> str:
    audio_file= open(input_filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt=prompt)
    return transcript


if __name__ == "__main__":
    args = parse_args()
    # Start recording
    transcript = transcribe(args.input_filename, prompt=args.prompt)
    print(transcript)
