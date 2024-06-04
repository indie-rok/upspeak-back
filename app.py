from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import requests
import tempfile
import logging
import uuid
import subprocess

from dotenv import load_dotenv
load_dotenv()

from split_audio_video import split_audio_video
from get_audio_transcript import get_audio_transcript, InsufficientWordsError
from process_audio_transcript import process_audio_transcript
from create_report_api import create_report_api
from prepare_video import prepare_video

app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)
SHARED_SECRET = os.getenv('SHARED_SECRET')

def validate_video():
    return False

def download_from_s3(video_url):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, str(uuid.uuid4()) + os.path.splitext(video_url)[1])

     # Download video from S3 using curl
    subprocess.run(['curl', '-o', temp_filename, video_url], check=True)

    return temp_filename


@app.route('/video_report', methods=['POST'])
def video_report():
    data = request.get_json()

    video_url = data.get('videoUrl')
    selected_topic = data.get('selectedTopic')
    auth_header = request.headers.get('Authorization')

    if auth_header != SHARED_SECRET:
        return jsonify({'error': 'Unauthorized'}), 401

    if not video_url:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        temp_local_video_path = download_from_s3(video_url)
        temp_prepared_video_path = prepare_video(temp_local_video_path)
        
        video_frames, audio_path = split_audio_video(temp_prepared_video_path)
        transcript = get_audio_transcript(audio_path)

        global_stats = process_audio_transcript(transcript)
        report = create_report_api(global_stats)

        report_content = {
            "topic": selected_topic.get("title") if selected_topic else None,
            "global_stats": global_stats,
            "report": report
        }

        return jsonify(report_content)
    except InsufficientWordsError as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print('error',e)
        logger.error(f"Error processing video: {str(e)}",  '\n')
        return jsonify({"error": "Error processing video"}), 500

@app.route('/test', methods=['get'])
def test():
    return jsonify({"working": True})