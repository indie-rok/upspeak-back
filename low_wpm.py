import shutil
import os
from split_in_chunks import split_in_chunks

def main():
    chunk_path = '/Users/20015296/Documents/python/audio-app/audio/chunk_audio/silences'
    audio_path = '/Users/20015296/Documents/python/audio-app/audio/full_audio/silences.mp3'
    
    if os.path.exists(chunk_path):
        shutil.rmtree(chunk_path)

    split_in_chunks(audio_path)

main()