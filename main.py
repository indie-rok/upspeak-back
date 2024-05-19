from split_audio_video import split_audio_video
from get_audio_transcript import get_audio_transcript
from process_audio_transcript import process_audio_transcript
from split_in_chunks import split_in_chunks
from process_chunks import process_chunks
from create_report import create_report

video_path = "/Users/20015296/Documents/python/audio-app/videos/pauses_2s.mov" 

def main():
    video_frames , audio_path = split_audio_video(video_path) # check to return duration and location of files
    transcript = get_audio_transcript(audio_path)
    global_stats = process_audio_transcript(transcript)
    chunk_folder, chunk_paths = split_in_chunks(audio_path)
    chunk_stats = process_chunks(chunk_paths, transcript)

    report_content = {
        "user_id": "asod-123",
        "mp3_location": "location.mp3",
        "track_length": 59.123,
        "global_stats": global_stats,
        "chunks": chunk_stats
    }

    create_report(audio_path,report_content)
    

main()