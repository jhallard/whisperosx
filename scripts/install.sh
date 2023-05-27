#!/usr/bin/env bash

# Install script for the entrypoint program and the actual script

cp ./../scripts/entrypoint.py $HOME/bin/entrypoint.py
cp ./../scripts/transcribe.py $HOME/bin/transcribe.py

chmod +x $HOME/bin/entrypoint.py
chmod +x $HOME/bin/transcribe.py
