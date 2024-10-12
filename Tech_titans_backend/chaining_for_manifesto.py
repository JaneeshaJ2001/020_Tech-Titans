import openai
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma
import json

def compare( user_input: str, client: openai.ChatCompletion):
    # System prompt for extraction
    system_prompt_agent2 = """
    You are an election manifesto comparison extractor. Based on the input, extract the candidate names and the comparison criteria mentioned. Return the information in the following format:

    - Candidate 1: [name of first candidate]
    - Candidate 2: [name of second candidate]
    - Comparison Criteria: [in what criteria the candidates are compared]

    If no criteria are mentioned, return "No specific criteria mentioned."
    """

    # Make the API request to Agent 2 (extractor)
    extraction_response = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": system_prompt_agent2},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )

    # Print the extracted candidate names and criteria
    print(extraction_response.choices[0].message.content)
    
    ###################################################################################################
    
    manifesto_extraction_result = extraction_response.choices[0].message.content

    chosen_candidates = []

    if "anura" in manifesto_extraction_result.lower():
        chosen_candidates.append("Anura Kumara Dissanayake")
    if "sajith" in manifesto_extraction_result.lower():
        chosen_candidates.append("Sajith Premadasa")
    if "ranil" in manifesto_extraction_result.lower():
        if not len(chosen_candidates) == 2:
            chosen_candidates.append("Ranil Wickremesinghe")
            
    print(chosen_candidates)

    # Extract the comparison criteria

    criteria_start = manifesto_extraction_result.find("Comparison Criteria:") + len("Comparison Criteria:")

    comparison_criteria = manifesto_extraction_result[criteria_start:].strip()

    print(comparison_criteria)

    # Function to dynamically select Chroma path based on input name.
    def select_chroma_path(person_name: str) -> str:
        # Map the person name to the respective database path.
        chroma_map = {
            "Sajith Premadasa": "sajith_data",
            "Anura Kumara Dissanayake": "anura_data",
            "Ranil Wickremesinghe": "ranil_data"
        }
        
        # Return the respective path based on the candidate's name.
        return chroma_map.get(person_name, "default_data")

    # Function to query the vector database and return the top 5 most similar documents.
    def query_rag_local(person_name: str, prompt: str):
        # Print the input query and the selected person.
        print(f"Querying vector database for {person_name} with prompt: '{prompt}'")
        
        # Dynamically select the Chroma database path based on the person's name.
        CHROMA_PATH = select_chroma_path(person_name)
        print(f"Selected CHROMA_PATH: {CHROMA_PATH}")

        # Prepare the embedding function and load the respective database.
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the database for relevant context (top 5 results).
        results = db.similarity_search_with_score(prompt, k=5)

        # # Print the top 5 most similar documents
        # print(f"\nTop 5 Similar Documents for {person_name}:")
        # for i, (doc, score) in enumerate(results):
        #     print(f"{i+1}. Document ID: {doc.metadata.get('id')}, Score: {score}")
        #     print(f"Content: {doc.page_content}\n")
        
        # Prepare the top 5 results as a list of dictionaries with '\n' replaced by spaces.
        top_documents = []
        for doc, score in results:
            top_documents.append({
                doc.page_content.replace("\n", " ")  # Replace newlines with spaces
            })

        return top_documents
        

    # Define the question prompt for comparison.
    prompt = comparison_criteria

    # Loop through each selected candidate and perform vector similarity search.
    candidate_1_data = query_rag_local(chosen_candidates[0], prompt)
    candidate_2_data = query_rag_local(chosen_candidates[1], prompt)

    # System prompt for comparison
    system_prompt_agent2 = """
    You are a comparison generator for political manifestos. Given the information about two candidates and specific comparison criteria, generate a concise 5-point comparison of their policies. Format the output as follows:

    Candidate 1 name: ##### , ##### , ##### , ##### , #####
    Candidate 2 name: ##### , ##### , ##### , ##### , #####
    """

    # Function to generate comparison using LLM
    def generate_comparison(candidate_1_name: str, candidate_1_data: str, candidate_2_name: str, candidate_2_data: str, comparison_criteria: str):
        # Prepare the input for the LLM
        comparison_input = (
            f"Comparison Criteria: {comparison_criteria}\n"
            f"Candidate 1 name: {candidate_1_name}\n"
            f"Candidate 1 data: {candidate_1_data}\n"
            f"Candidate 2 name: {candidate_2_name}\n"
            f"Candidate 2 data: {candidate_2_data}"
        )

        # Make the API request to Agent 2 (comparison generator)
        comparison_response = client.chat.completions.create(
            model="model-identifier",  # Replace with your model identifier
            messages=[
                {"role": "system", "content": system_prompt_agent2},
                {"role": "user", "content": comparison_input}
            ],
            temperature=0.7,
        )

        # Get the comparison result
        comparison_result = comparison_response.choices[0].message.content.strip()
        return comparison_result

    # Generate the comparison
    comparison_output = generate_comparison(chosen_candidates[0], candidate_1_data, chosen_candidates[1], candidate_2_data, comparison_criteria)

    # Print the formatted comparison result
    print("Comparison Result:\n", comparison_output)

    # System prompt for classification
    system_prompt_agent3 = """
    You are a JSON formatter. Given a formatted comparison string of two candidates' policies, extract the information into a JSON object with the following structure:

    {
        "Candidate 1 name": ["Full point 1", "Full point 2", "Full point 3", "Full point 4", "Full point 5"],
        "Candidate 2 name": ["Full point 1", "Full point 2", "Full point 3", "Full point 4", "Full point 5"]
    }

    Return the JSON as a string.
    """

    # Function to call Agent 3 for extracting output into JSON format
    def extract_to_json(comparison_result: str):
        # Prepare the input for Agent 3
        json_input = comparison_result.strip()

        # Make the API request to Agent 3 (JSON formatter)
        json_response = client.chat.completions.create(
            model="model-identifier",  # Replace with your model identifier
            messages=[
                {"role": "system", "content": system_prompt_agent3},
                {"role": "user", "content": json_input}
            ],
            temperature=0.7,
        )

        # Get the JSON result
        json_result = json_response.choices[0].message.content.strip()
        
        # Parse the JSON string into a Python dictionary
        return json_result

    # Function to save JSON to a file
    def save_json_to_file(json_data, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
            
    # Extract the comparison output to JSON
    comparison_json = extract_to_json(comparison_output)
    
    parsed_json = json.loads(comparison_json)

    # Optionally manipulate the parsed JSON (if needed)
    # For example, cleaning up or replacing certain values
    # Here, I'm assuming no manipulation is required.
    
    # Convert back to JSON string if needed
    comparison_json = json.dumps(parsed_json)

    # Save the formatted JSON result to a file
    save_json_to_file(comparison_json, 'comparison_output.json')