from queue import Queue
import threading
import sounddevice as sd


CONFIG = {
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

audio_thread = threading.Thread(target=process_audio, daemon=True)
audio_thread.start()