import subprocess
import uuid
import os
import tempfile

def prepare_video(input_path):
    temp_dir = tempfile.mkdtemp()
    processed_filename = os.path.join(temp_dir, str(uuid.uuid4()) + os.path.splitext(input_path)[1])

    # Use FFmpeg to re-encode the video and add metadata
    try:
        command = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
            '-c:a', 'aac', '-b:a', '128k',
            '-movflags', 'faststart',  # Optimize for streaming
            '-metadata', 'title="My Video"',
            processed_filename
        ]

        subprocess.run(command, check=True)

        return processed_filename

    except Exception as e:
        print(f"Error processing video: {e}")
        raise