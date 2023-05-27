# WhisperOSX

A simple collection of scripts that provide speech-to-text functionality across the desktop. Press a 
hotkey to start recording, press the hotkey again to stop recording, and have your speech rendered speech rendered
to high-quality text quickly and effortlessly.

## Quickstart

**Enter instructions here for building and running**

These scripts require:

**Programs**
- `ffmpeg`: to pull audio from your microphone

**Brew**
- `portaudio`: `$ brew install portaudio` (required for `pyaudio`)

**Python Modules**
- `pyautogui`: to create keystokes in the GUI from a string of text
- `openai`: to send audio to the OpenAI Whipser API

## Why?

With the release of [Whipser](https://openai.com/research/whisper), speech-to-text is good enough that it should be ubiquitous. However, most
users of the Apple ecosystem are still forced to suffer through Siri's crappy speech-to-text functionality. This is unacceptable.

I created these scripts so that I could have access to world-class speech-to-text functionality anywhere on my desktop at anytime.

## Future Work

Ideally this would run entirely locally using the [WhisperCpp](github.com/ggerganov/whisper.cpp) project. However, at the time
I created this project I was running on Intel silicon and inference is too slow to reasonably make use of.
