import os
import shutil
from subprocess import CalledProcessError, run
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection

# Load the model and pipeline
model = Model.from_pretrained("pyannote/segmentation", use_auth_token="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")
pipeline = VoiceActivityDetection(segmentation=model)
HYPER_PARAMETERS = {
  "onset": 0.5,
  "offset": 0.5,
  "min_duration_on": 2,
  "min_duration_off": 2
}
pipeline.instantiate(HYPER_PARAMETERS)

def split_audio(input_file, output_file, start, end):
    length = end - start
    cmd = [
        "ffmpeg", "-ss", str(start), "-i", input_file, "-t", str(length), 
        "-vn", "-acodec", "libmp3lame", "-ar", "48000", "-ac", "1", output_file
    ]
    try:
        run(cmd, capture_output=True, check=True).stdout
    except CalledProcessError as e:
        raise RuntimeError(f"FFMPEG error: {str(e)}")

def split_in_chunks(audio_path):
    try:
        vad = pipeline(audio_path)

        # Extract the base name of the file to create a unique folder
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_dir = os.path.join("audio", "chunk_audio", base_name)
        os.makedirs(output_dir, exist_ok=True)

        chunk_paths = []
        count = 1
        for turn, _ in vad.itertracks(yield_label=False):
            start = turn.start
            end = turn.end
            filename = os.path.join(output_dir, f"chunk-{count}.mp3")
            split_audio(audio_path, filename, start, end)
            chunk_paths.append((filename, start, end))
            print(f"Created {filename} from {start} to {end} seconds")
            count += 1

        return output_dir, chunk_paths
    except Exception as e:
        print(f"An error occurred while splitting the audio: {e}")
        return None
