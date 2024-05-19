def get_wpm(total_words, duration_seconds):
    duration_minutes = duration_seconds / 60
    return total_words / duration_minutes if duration_minutes > 0 else 0

