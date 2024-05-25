# cost_calculations.py

def calculate_transcription_cost(json_data, cost_per_second=0.0001):
    total_seconds = sum(memo['length'] for memo in json_data.values() if memo['transcription'] == "Transcription of the audio file.")
    print(str(total_seconds) + " seconds total. this is " + str(total_seconds/60) + " minutes.")
    total_cost = total_seconds * cost_per_second
    return total_cost

# # Usage example:
# json_filename = "/Users/zizo/Documents/code/brain/db.json"
#
# # Assuming existing_data is your loaded JSON data
# existing_data = load_json_data(json_filename)
# estimated_cost = calculate_transcription_cost(existing_data)
#
# print(f"Estimated transcription cost: ${estimated_cost:.2f}")
