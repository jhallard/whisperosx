# WhisperOSX

A simple collection of scripts that provide speech-to-text functionality across the desktop. Press a 
hotkey to start recording, press the hotkey again to stop recording, and have your speech rendered speech rendered
to high-quality text quickly and effortlessly.

## Status

I wrote this project in an hour or so in an attempt to experiment with the OpenAI API and some OSX automation APIs
in my free time.

**This project almost kinda works**, but it's not great. I have it set up such that I can trigger recording with a hotkey 
combination (`Ctrl-Shift-7`) and can trigger stop-recording with the same combination, the resulting audio clip is then 
sent to the OpenAI Whisper API where it's transcribed, and the transcription is then written through a virtual keyboard
to whatever program I currently have open.

However, OSX's protections mean that any program you have open when you run that automation needs both microphone access 
and Accessibility API access, and providing those can be a pain. It's also a bit slow to begin recording, so it's not clear
when you  should start talking after pressing the hotkeys. 

I'm basically giving up on this for now, but it does mostly work.

## Quickstart

**Enter instructions here for building and running**

These scripts require:

**Brew**
- `portaudio`: `$ brew install portaudio` (required for `pyaudio`)

**Python Modules**
- `pyautogui`: to create keystokes in the GUI from a string of text
- `openai`: to send audio to the OpenAI Whipser API
- `pyaudio`: for capturing audio from the active microphone
- `openai>=0.27.0`: transcribing audio to text
- `psutil`: finding an actively running process

## Why?

With the release of [Whipser](https://openai.com/research/whisper), speech-to-text is good enough that it should be ubiquitous. However, most
users of the Apple ecosystem are still forced to suffer through Siri's crappy speech-to-text functionality. This is unacceptable.

I created these scripts so that I could have access to world-class speech-to-text functionality anywhere on my desktop at anytime.

## Future Work

Ideally this would run entirely locally using the [WhisperCpp](github.com/ggerganov/whisper.cpp) project. However, at the time
I created this project I was running on Intel silicon and inference is too slow to reasonably make use of.
