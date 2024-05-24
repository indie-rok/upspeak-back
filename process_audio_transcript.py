from get_wpm import get_wpm

def process_audio_transcript(transcription):
    silence_count = 0
    filler_word_count = 0
    total_words = len(transcription.words)
    
    # Keep this as a set for fast lookups
    filler_words_set = {
        "I was like", "was like", "I'm like", "you know what I mean", "kind of", "um", "ah", "huh", "and so", "so um", "uh", 
        "and um", "like um", "so like", "like it's", "it's like", "i mean", "yeah", "ok so", "uh so", "so uh", "yeah so", 
        "you know", "it's uh", "uh and", "and uh", "like", "kind", "basically", "literally", "actually", "well", 
        "sort of", "you see", "I guess", "uh"
    }

    # Create an empty list to store found filler words
    filler_words_list = []

    # Calculate silences and filler words
    for i in range(len(transcription.words) - 1):
        current_word = transcription.words[i]
        next_word = transcription.words[i + 1]

        # Calculate the gap between the end of the current word and the start of the next word
        silence_duration = next_word['start'] - current_word['end']
        if (silence_duration >= 1.0):
            silence_count += 1

        # Check if the current word is a filler word
        if (current_word['word'].lower() in filler_words_set):
            filler_word_count += 1
            filler_words_list.append(current_word['word'].lower())

    # Also check the last word for being a filler word
    if (transcription.words[-1]['word'].lower() in filler_words_set):
        filler_word_count += 1
        filler_words_list.append(transcription.words[-1]['word'].lower())

    # Calculate average WPM (Words Per Minute)
    average_wpm = get_wpm(total_words, transcription.duration)

    return {
        "silence_count": silence_count,
        "filler_word_count": filler_word_count,
        "average_wpm": average_wpm,
        "filler_words": filler_words_list
    }