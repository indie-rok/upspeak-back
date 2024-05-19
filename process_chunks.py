from get_wpm import get_wpm

def process_chunks(chunk_paths, transcript):
    
    chunk_stats = []

    for idx, (chunk_path, start, end) in enumerate(chunk_paths):
        # Calculate WPM for the chunk
        words_in_chunk = [word for word in transcript.words if start <= word['start'] < end]
        total_words = len(words_in_chunk)
        duration_seconds = end - start
        wpm = get_wpm(total_words, duration_seconds)

        chunk_stats.append({
            "id": idx + 1,
            "start": start,
            "end": end,
            "wpm": wpm
        })

    return chunk_stats
