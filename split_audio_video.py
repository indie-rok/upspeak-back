import os
import cv2
from moviepy.editor import VideoFileClip
import base64
import tempfile
import logging

logger = logging.getLogger(__name__)

def split_audio_video(video_path, seconds_per_frame=2):
    try:
        base64Frames = []
        file_name = os.path.basename(video_path)
        file_name_without_extension, extension = os.path.splitext(file_name)

        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        frames_to_skip = int(fps * seconds_per_frame)
        curr_frame = 0

        # Loop through the video and extract frames at specified sampling rate
        while curr_frame < total_frames - 1:
            video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
            curr_frame += frames_to_skip
        video.release()

        # Extract audio from video and store it temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_path = temp_audio_file.name
        
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(temp_audio_path, bitrate="32k")
        clip.audio.close()
        clip.close()

        logger.info(f"Extracted {len(base64Frames)} frames")
        logger.info(f"Extracted audio to {temp_audio_path}")

        return base64Frames, temp_audio_path
    except Exception as e:
        print(f"Error spliting video: {e}")
        raise
