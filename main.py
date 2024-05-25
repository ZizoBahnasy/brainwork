# main.py

from memo_processing import (
    load_json_data,
    save_to_json,
    process_source_directory,
    transcribe_all_unprocessed_memos
)

def main():
    memos_directory = "/Users/zizo/Documents/code/brain/memos"
    json_filename = "/Users/zizo/Documents/code/brain/db.json"

    # Load existing data
    existing_data = load_json_data(json_filename)

    while True:
        print("Enter the path of a source directory (or type 'done' to finish):")
        source_dir_input = input().strip()

        # for ease of testing
        if source_dir_input == '1':
            source_dir_input = "/Users/zizo/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"

        elif source_dir_input == '2':
            source_dir_input = "/Users/zizo/Documents/From S1/Downloads 4:27/Zizo's Voice Memos"

        elif source_dir_input.lower() == 'done':
            break

        existing_data = process_source_directory(source_dir_input, memos_directory, existing_data)
        print("Directory processed. You can enter another directory.")

# After processing all directories, start transcription process
    transcribe_all_unprocessed_memos(existing_data, memos_directory, json_filename)

    # Save the updated data to JSON
    save_to_json(existing_data, json_filename)
    print(f"Data updated and saved to {json_filename}")

if __name__ == "__main__":
    main()
