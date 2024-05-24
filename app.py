from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from dotenv import load_dotenv
load_dotenv()

from split_audio_video import split_audio_video
from get_audio_transcript import get_audio_transcript
from process_audio_transcript import process_audio_transcript
from create_report_api import create_report_api
from prepare_video import prepare_video

app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)

def validate_video():
    return False

@app.route('/video_report', methods=['POST'])
def video_report():
    try:
        video = request.files.get('video_file')
        topic = request.form.get('topic')
    except Exception as e:
        logger.info("error getting the files:", {str(e)}, '\n')
        return jsonify({"error": "Failed to get files or form data"}), 400

    if not video:
        return jsonify({"error": "No video provided"}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_video_path = os.path.join(temp_dir, secure_filename(video.filename))
            video.save(temp_video_path)

            # Process the video to ensure proper metadata
            processed_video_path = os.path.join(temp_dir, "processed_" + secure_filename(video.filename))
            prepare_video(temp_video_path, processed_video_path)

            video_frames, audio_path = split_audio_video(processed_video_path)
            transcript = get_audio_transcript(audio_path)
            global_stats = process_audio_transcript(transcript)
            report = create_report_api(global_stats)

            report_content = {
                "topic": topic,
                "global_stats": global_stats,
                "report": report
            }

            return jsonify(report_content)
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}",  '\n')
        return jsonify({"error": str(e)}), 500