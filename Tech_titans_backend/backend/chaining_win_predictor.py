import openai
import json

def win_predictor(user_input: str, client: openai.ChatCompletion):
    # System prompt for Agent 1: Candidate extractor
    system_prompt_agent1 = """
    You are a candidate extractor for an election prediction tool. Based on the user input, extract the names of the candidates mentioned. Return the information in the following format:

    - Candidates: [list of names of the candidates]

    If no candidates are mentioned, return "No candidates mentioned."
    """

    # Make the API request to Agent 1 (candidate extractor)
    extraction_response = client.chat.completions.create(
        model="model-identifier",  # Replace with your model identifier
        messages=[
            {"role": "system", "content": system_prompt_agent1},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )

    # Print the extracted candidate names
    print(extraction_response.choices[0].message.content)

    # Extract the candidate names from the response
    extracted_candidates = extraction_response.choices[0].message.content

    # System prompt for Agent 2: JSON formatter
    system_prompt_agent2 = """
    You are a JSON formatter. Given a list of candidates extracted from the user input, format the output into a JSON object with the following structure:

    {
        "candidates": ["name1", "name2", "name3", ...]
    }

    Return the JSON object as a string.
    """

    # Make the API request to Agent 2 (JSON formatter)
    json_response = client.chat.completions.create(
        model="model-identifier",  # Replace with your model identifier
        messages=[
            {"role": "system", "content": system_prompt_agent2},
            {"role": "user", "content": extracted_candidates}
        ],
        temperature=0.7,
    )

    # Extract the JSON response
    json_output = json_response.choices[0].message.content.strip()

    # Print the JSON result
    print("JSON Output:\n", json_output)

    # Function to save JSON to a file
    def save_json_to_file(json_data, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

    # Parse the JSON string into a Python dictionary
    json_data = json.loads(json_output)

    # Save the formatted JSON result to a file
    save_json_to_file(json_data, 'candidates_output.json')

    return json_data
