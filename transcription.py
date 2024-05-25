# transcription.py

import whisper
from datetime import datetime
import time

def transcribe_memo(memo_path, audio_length):
    model = whisper.load_model("large")  # Adjust the model size as needed

    start_time = time.time()  # Start timing

    audio = whisper.load_audio(memo_path)
    result = model.transcribe(audio)

    end_time = time.time()  # End timing
    transcription_duration = end_time - start_time

    print(f"Transcription of {memo_path} (length: {audio_length:.2f} seconds) took {transcription_duration:.2f} seconds. This is {(audio_length/transcription_duration):.2f} seconds of audio transcribed per second.")

    return result["text"]


def save_transcription_to_file(transcription, filename, header):
    # Trim leading/trailing whitespace from the header and transcription
    header = header.strip()
    transcription = transcription.strip()

    # Concatenate header and transcription with a newline in between
    full_text = header + "\n\n" + transcription

    with open(filename, 'w') as file:
        file.write(full_text)

    # Print the transcription as it's saved
    print(f"\nTranscription saved to {filename}:\n{full_text}\n")

def get_header_for_transcription(memo_info):
    try:
        # Convert the datetime string back to a datetime object
        datetime_obj = datetime.strptime(memo_info['datetime'], "%Y-%m-%d %H:%M:%S")
        datetime_str = datetime_obj.strftime("%B %d, %Y at %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.")
    except (TypeError, ValueError):
        datetime_str = "Unknown Date"

    # Format length to two decimal places
    length_str = f"{memo_info['length']:.2f} seconds" if memo_info['length'] else "Unknown Length"
    header = f"Date: {datetime_str}\nLength: {length_str}"
    return header
