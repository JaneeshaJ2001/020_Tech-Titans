import openai
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma
import json

def sentiment_analysis(user_input: str, client: openai.ChatCompletion):
    # Agent 1: Extract Candidates
    system_prompt_agent1 = """
    You are a sentiment analysis candidate extractor. Based on the input, extract the candidate names mentioned. Return the information in the following format:

    - Candidates: [list of candidate names]

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

    # Print the extracted candidate names
    candidates_extracted = extraction_response_agent1.choices[0].message.content
    print(candidates_extracted)
    
    ###################################################################################################
    
    # Agent 2: Extract Comparison Criteria (e.g., Facebook posts, Twitter posts)
    system_prompt_agent2 = """
    You are a sentiment analysis criteria extractor. Based on the input, extract the criteria used to compare the sentiment, such as Facebook posts, Twitter posts, news articles, etc. Return the information in the following format:

    - Criteria: [list of criteria]

    If no criteria are mentioned, return "No specific criteria mentioned."
    """

    # Make the API request to Agent 2 (criteria extractor)
    extraction_response_agent2 = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": system_prompt_agent2},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )

    # Print the extracted criteria
    criteria_extracted = extraction_response_agent2.choices[0].message.content
    print(criteria_extracted)
    
    ###################################################################################################

    # Agent 3: Create JSON from extracted data
    system_prompt_agent3 = """
    You are a JSON formatter. Given the extracted candidates and criteria, create a JSON object with the following structure:

    {
        "Candidates": [list of candidate names],
        "Criteria": [list of criteria]
    }

    Return the JSON as a string.
    """

    # Prepare the input for Agent 3 (JSON creation)
    json_input = f"Candidates: {candidates_extracted}\nCriteria: {criteria_extracted}"

    # Make the API request to Agent 3 (JSON formatter)
    json_response_agent3 = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": system_prompt_agent3},
            {"role": "user", "content": json_input}
        ],
        temperature=0.7,
    )

    # Get the JSON result
    json_result = json_response_agent3.choices[0].message.content.strip()

    # Print the JSON result
    print("Generated JSON:\n", json_result)

    # Save the JSON result to a file
    with open('sentiment_analysis_output.json', 'w') as json_file:
        json.dump(json.loads(json_result), json_file, indent=4)