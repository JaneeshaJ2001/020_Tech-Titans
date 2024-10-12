import openai
import json
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma

def chat_function(user_input: str, client: openai.ChatCompletion):
    # System prompt for extracting candidate names
    system_prompt_extractor = """
    You are an election manifesto extractor. Based on the input, extract the candidate names mentioned. Return them as a comma-separated list.
    """

    # Make the API request to Agent 1 (extractor)
    extraction_response = client.chat.completions.create(
        model="model-identifier",  # Replace with your model identifier
        messages=[
            {"role": "system", "content": system_prompt_extractor},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )

    # Extract candidate names from the response
    candidates = extraction_response.choices[0].message.content.strip().split(',')
    candidates = [candidate.strip() for candidate in candidates if candidate.strip()]

    print(f"Extracted Candidates: {candidates}")

    # Prepare the question by removing candidate names from the user input
    for candidate in candidates:
        user_input = user_input.replace(candidate, '')

    question = user_input.strip()

    # Function to dynamically select Chroma path based on candidate name.
    def select_chroma_path(person_name: str) -> str:
        chroma_map = {
            "Sajith Premadasa": "sajith_data",
            "Anura Kumara Dissanayake": "anura_data",
            "Ranil Wickremesinghe": "ranil_data"
        }
        return chroma_map.get(person_name, "default_data")

    # Function to query the vector database and return the top 5 most similar documents.
    def query_rag_local(person_name: str, question: str):
        print(f"Querying vector database for {person_name} with question: '{question}'")
        CHROMA_PATH = select_chroma_path(person_name)
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        results = db.similarity_search_with_score(question, k=5)

        # Prepare the top 5 results
        top_documents = []
        for doc, score in results:
            top_documents.append(doc.page_content.replace("\n", " "))
        return top_documents

    # Collect data for each candidate
    candidate_data = {}
    for candidate in candidates:
        candidate_data[candidate] = query_rag_local(candidate, question)

    # System prompt for generating an answer
    system_prompt_answer_generator = """
    You are an answer generator based on provided context. Given the question and relevant data for each candidate, generate a concise answer.
    """

    # Prepare the input for Agent 3
    answer_input = f"Question: {question}\n"
    for candidate in candidates:
        answer_input += f"{candidate} data: {', '.join(candidate_data[candidate])}\n"

    # Make the API request to Agent 3 (answer generator)
    answer_response = client.chat.completions.create(
        model="model-identifier",  # Replace with your model identifier
        messages=[
            {"role": "system", "content": system_prompt_answer_generator},
            {"role": "user", "content": answer_input}
        ],
        temperature=0.7,
    )

    # Get the answer result
    answer_result = answer_response.choices[0].message.content.strip()
    print(f"Generated Answer:\n{answer_result}")

    # System prompt for formatting the answer into JSON
    system_prompt_json_formatter = """
    You are a JSON formatter. Given an answer string, convert it into a JSON object with the following structure:

    {
        "Answer": "Your answer here"
    }

    Return the JSON as a string.
    """

    # Function to format the answer into JSON
    def format_answer_to_json(answer: str):
        json_input = answer.strip()
        json_response = client.chat.completions.create(
            model="model-identifier",  # Replace with your model identifier
            messages=[
                {"role": "system", "content": system_prompt_json_formatter},
                {"role": "user", "content": json_input}
            ],
            temperature=0.7,
        )
        return json_response.choices[0].message.content.strip()

    # Format the generated answer into JSON
    answer_json = format_answer_to_json(answer_result)

    # Save the JSON to a file
    def save_json_to_file(json_data, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
            
    answer_json = '{' + answer_json.split('{')[1].split('}')[0].replace('\n','').replace('\"','"') + '}'
    # # Parse the JSON string
    # parsed_json = json.loads(answer_json)

    # # Optionally manipulate the parsed JSON (if needed)
    # # For example, cleaning up or replacing certain values
    # # Here, I'm assuming no manipulation is required.
    
    # # Convert back to JSON string if needed
    # answer_json = json.dumps(parsed_json)
    

    # Save the JSON output
    save_json_to_file(answer_json, 'answer_output.json')
    
        
    ################################################################################
    
    #Question generation agent
    
    
    def generate_questions(client: openai.ChatCompletion, conversation_context: str):
        # System prompt for generating questions
        system_prompt_question_generator = """
        You are a question generator. Based on the conversation context provided, generate a list of potential follow-up questions for the user to choose from consis.
        Return the questions in the following JSON format:
        {
            "questions": ["Question 1", "Question 2", "Question 3", ...]
        }
        """

        # Make the API request to generate questions
        question_generation_response = client.chat.completions.create(
            model="model-identifier",  # Replace with your model identifier
            messages=[
                {"role": "system", "content": system_prompt_question_generator},
                {"role": "user", "content": conversation_context}
            ],
            temperature=0.7,
        )

        # Extract the generated questions
        generated_questions_json = question_generation_response.choices[0].message.content.strip()

        # Function to save the questions JSON to a file
        def save_questions_to_file(questions_json, file_name):
            with open(file_name, 'w') as json_file:
                json.dump(json.loads(questions_json), json_file, indent=4)

        # Save the generated questions to a file
        save_questions_to_file(generated_questions_json, 'generated_questions.json')

        print(f"Generated Questions:\n{generated_questions_json}")

    # Example usage:
    generate_questions(client, user_input)

    
    

