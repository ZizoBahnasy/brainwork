# memo_processing.py

import os
import shutil
from mutagen.mp4 import MP4
from datetime import datetime
import json

from transcription import (
    transcribe_memo,
    save_transcription_to_file,
    get_header_for_transcription
)

def sync_voice_memos(source_dir, target_dir):
    # Ensure target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Check if the source directory is valid
    if not os.path.isdir(source_dir):
        print(f"Source directory not found: {source_dir}")
        return

    # Iterate over all .m4a files in the source directory
    for filename in os.listdir(source_dir):
        if filename.endswith(".m4a"):
            source_file = os.path.join(source_dir, filename)
            target_file = os.path.join(target_dir, filename)

            # Copy file if it doesn't exist in the target directory
            if not os.path.exists(target_file):
                shutil.copy2(source_file, target_file)
                print(f"Copied '{filename}' to {target_dir}")

def get_voice_memo_info(file_path):
    try:
        audio = MP4(file_path)
        length = audio.info.length  # Length in seconds
        return length
    except:
        print(f"Error processing file: {file_path}")
        return None

def parse_datetime_from_filename(filename):
    try:
        # Remove the file extension and split at the hyphen
        date_time_str = filename.split('.')[0].split('-')[0]
        # Parse the date and time
        return datetime.strptime(date_time_str, "%Y%m%d %H%M%S")
    except ValueError:
        return None  # In case the date and time are not in the expected format

def get_files(directory, existing_data):
    new_voice_memos = []
    try:
        # Get all .m4a files and sort them
        files = sorted([f for f in os.listdir(directory) if f.endswith(".m4a")])

        for filename in files:
            file_path = os.path.join(directory, filename)
            date_time = parse_datetime_from_filename(filename)
            # Extract date and time from filename
            length = get_voice_memo_info(file_path)

            if filename not in existing_data:
                # New memo, initialize data
                memo_info = {
                    "saved_title": filename,
                    "datetime": date_time,
                    "length": length,
                    "transcription": "",
                    "summary": "",
                    "keywords": [],
                    "generated_title": "",
                    "file": file_path
                }
                new_voice_memos.append(memo_info)
            else:
                # Existing memo, keep existing data
                new_voice_memos.append(existing_data[filename])

    except Exception as e:
        print(f"An error occurred: {e}")

    return new_voice_memos

def load_json_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, default=str)  # 'default=str' to handle datetime objects

def update_voice_memo_data(existing_data, voice_memos):
    # Update existing data with new voice memos
    for memo in voice_memos:
        existing_data[memo['saved_title']] = memo

    # Remove entries for deleted voice memos
    existing_titles = set(memo['saved_title'] for memo in voice_memos)
    titles_to_delete = [title for title in existing_data if title not in existing_titles]
    for title in titles_to_delete:
        del existing_data[title]

    return existing_data

def process_source_directory(source_dir, target_dir, existing_data):
    if os.path.isdir(source_dir):
        sync_voice_memos(source_dir, target_dir)
        voice_memos_data = get_files(target_dir, existing_data)

        # Update existing data with new and updated voice memos
        for memo in voice_memos_data:
            existing_data[memo['saved_title']] = memo

        # Remove entries for deleted voice memos
        existing_titles = set(memo['saved_title'] for memo in voice_memos_data)
        titles_to_delete = [title for title in existing_data if title not in existing_titles]
        for title in titles_to_delete:
            del existing_data[title]

        return existing_data

    else:
        print(f"Path not found: {source_dir}. Please enter a valid directory path.")
        return existing_data

def transcribe_all_unprocessed_memos(existing_data, memos_directory, json_filename):
    transcriptions_dir = os.path.join(memos_directory, "transcriptions")
    os.makedirs(transcriptions_dir, exist_ok=True)
    # print("transcription folder set up")

    for memo in existing_data.values():
        if memo['transcription'] == '':
            print(f"Processing transcription for: {memo['saved_title']}")
            # print(memo)
            # Transcribe the voice memo
            transcription = transcribe_memo(memo['file'], memo['length'])
            # print("reprinting transcription: " + transcription)
            memo['transcription'] = transcription

            # Save the transcription as a text file
            txt_filename = os.path.splitext(os.path.basename(memo['file']))[0] + ".txt"
            txt_filepath = os.path.join(transcriptions_dir, txt_filename)
            header = get_header_for_transcription(memo)
            save_transcription_to_file(transcription, txt_filepath, header)

            # Save updated data to JSON after each transcription
            save_to_json(existing_data, json_filename)
        else:
            print(memo['saved_title'] + " has already been transcribed.")
