import subprocess

def prepare_video(input_path, output_path):
    # Use FFmpeg to re-encode the video and add metadata
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '128k',
        '-movflags', 'faststart',  # Optimize for streaming
        '-metadata', 'title="My Video"',
        output_path
    ]

    subprocess.run(command, check=True)