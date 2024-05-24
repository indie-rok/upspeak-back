def create_report_api(global_stats):
    # Extract global stats
    words_per_minute = global_stats["average_wpm"]
    number_of_silences = global_stats["silence_count"]
    filler_words = global_stats["filler_words"]
    filler_word_count = global_stats["filler_word_count"]
    
    # Calculate voice speed score
    optimal_wpm = 155
    speed_score = max(0, 100 - abs(optimal_wpm - words_per_minute))
    speed_score = round(speed_score)
    speed_feedback = (
        f"Your speaking speed is {words_per_minute:.2f} WPM. The optimal target is {optimal_wpm} WPM. "
        "Speaking too quickly or too slowly can affect your clarity and effectiveness."
    )
    
    # Calculate silences score
    ideal_silences = 3
    silence_score_component = max(0, 100 - abs(ideal_silences - number_of_silences) * 10)
    filler_words_score_component = max(0, 100 - filler_word_count * 10)
    
    silences_score = min(silence_score_component, filler_words_score_component)
    silences_score = round(silences_score)
    silences_feedback = (
        f"You had {number_of_silences} silences. "
        "The ideal number of silences is 3. Try adding silences to your speech every 2 or 3 phrases. 1.5 seconds is the ideal silence length."
    )

    filler_word_feedback = (
        f"You used {filler_word_count} filler word(s) ({', '.join(filler_words)}). "
        "Filler words are used instead of silences. "
    )
    
    # Create the report
    report = {
        "voice_speed": {
            "title": "Voice Speed",
            "score": speed_score,
            "criteria": [
                {
                    "title": "Words per minute",
                    "value": round(words_per_minute),
                    "feedback": speed_feedback
                }
            ]
        },
        "silences": {
            "title": "Silences",
            "score": silences_score,
            "criteria": [
                {
                    "title": "Number of silences",
                    "value": number_of_silences,
                    "feedback": silences_feedback
                },
                {
                    "title": "Number of filler words",
                    "value": filler_word_count,
                    "feedback": filler_word_feedback
                }
            ]
        }
    }
    
    return report
