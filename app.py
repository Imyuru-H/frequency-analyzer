#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Imyuru_. Licensed under MIT License.

__version__ = '0.0.0'
__author__ = 'Imyuru_'

import os
import sys
import threading
import time
import logging
from queue import Queue

import numpy as np
import sounddevice as sd


CONFIG = {
    "window scale": 0.6,
    "W-H ratio": 16/9,
    "FORMAT": 'float32',   # Audio format
    "CHANNELS": 1,         # Number of channels (1=mono, 2=stereo)
    "SAMPLE_RATE": 44100,  # Sample rate
    "CHUNK_SIZE": 256      # Chunk size
}


audio_queue = Queue()

def audio_callback(indata, frames, time, status):
    """Audio stream callback function
    - indata: Audio data chunk (shape=(frames, channels))
    - frames: Number of frames in the current chunk
    - time: Time information
    - status: Error status
    """
    if status:
        print(f"Audio stream error: {status}")

    # Directly get the raw audio stream data
    audio_queue.put(indata.copy())
    
def process_audio():
    """Independent thread for processing audio data"""
    global input_stream
    
    input_stream.start()
    
    while True:
        data = audio_queue.get()
        # Processing logic
        print(f"Processing audio chunk: {data}")

# Start capturing audio stream
input_stream = sd.InputStream(
    samplerate=CONFIG["SAMPLE_RATE"],
    channels=CONFIG["CHANNELS"],
    blocksize=CONFIG["CHUNK_SIZE"],
    callback=audio_callback,
    dtype=CONFIG["FORMAT"]
)
input_stream.start()


class Analyzer:
    def __init__(self):
        self.window_scale = CONFIG["window scale"]
        self.height = int(self.width / CONFIG["W-H ratio"])
        self.width = 1920
        
        self.audio_thread = threading.Thread(target=process_audio, daemon=True)
    
    def _start(self):
        pass