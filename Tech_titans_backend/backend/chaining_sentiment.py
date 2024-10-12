import openai
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma
import json

def sentiment_analysis(user_input: str, client: openai.ChatCompletion):
    # Agent 1: Extract Candidates and Sentiments
    system_prompt_agent1 = """
    You are a sentiment analysis data extractor. Based on the input, extract the candidate names and their sentiment percentages (positive, negative, neutral) in the following format:

    - {candidate_name}: [positive_percentage, negative_percentage, neutral_percentage]

    If no candidates are mentioned, return "No candidates found."
    """

    # Make the API request to Agent 1 (extractor)
    extraction_response_agent1 = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": system_prompt_agent1},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )

    # Extract the sentiment analysis data
    sentiment_data = extraction_response_agent1.choices[0].message.content
    print(sentiment_data)
    
    ###################################################################################################

    # Agent 2: Create JSON from extracted data
    system_prompt_agent2 = """
    You are a JSON formatter. Given the extracted candidate names and their sentiment percentages, create a JSON object with the following structure:

    {
        "candidate1 name": [positive, negative, neutral],
        "candidate2 name": [positive, negative, neutral]
    }

    Return the JSON as a string.
    """

    # Prepare the input for Agent 2 (JSON creation)
    json_input = sentiment_data

    # Make the API request to Agent 2 (JSON formatter)
    json_response_agent2 = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": system_prompt_agent2},
            {"role": "user", "content": json_input}
        ],
        temperature=0.7,
    )

    # Get the JSON result
    json_result = json_response_agent2.choices[0].message.content.strip()

    # Print the JSON result
    print("Generated JSON:\n", json_result)

    # # Save the JSON result to a file
    # with open('sentiment_analysis_output.json', 'w') as json_file:
    #     json.dump(json.loads(json_result), json_file, indent=4)
        
           # Function to save JSON to a file
    def save_json_to_file(json_data, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
            
    # # Extract the comparison output to JSON
    # comparison_json = extract_to_json(comparison_output)

    # Save the formatted JSON result to a file
    save_json_to_file(json_result, 'sentiment_analysis_output.json')
