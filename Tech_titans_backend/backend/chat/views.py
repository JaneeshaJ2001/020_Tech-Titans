from django.http import JsonResponse
from django.views import View
from openai import OpenAI
from langchain.vectorstores.chroma import Chroma
import json
import chaining_for_manifesto
import chaining_Chat_bot
import chaining_sentiment
import chaining_win_predictor
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
import os
import re

def extract_json_from_string(input_string: str):
    # Use regex to find the JSON-like structure in the string
    json_pattern = r'\{.*?\}'
    json_match = re.search(json_pattern, input_string, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(0)  # Extract the matched JSON string
        try:
            # Parse the JSON string into a Python dictionary
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON")
            return None
    else:
        print("Error: No JSON found in the input string")
        return None

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings



class ChatView(View):
    def get(self, request):
         
        # Point to the local server
        client = OpenAI(base_url="http://192.168.137.1:1234/v1", api_key="lm-studio")

        system_prompt_agent1 = """
        You are an election-related task classifier. For each prompt entered, you must categorize it into one of the following categories and return only the category name:

        1. Chat Bot: If the input involves general conversation, Q&A, or interactive dialogue without a specific analysis or comparison task.
        2. Semantic Analysis: If the input is related to social media content analysis.
        3. Win Predictor: If the input is related to predicting election outcomes based on polling data, trends, or performance metrics.
        4. Manifesto Comparator: If the input involves comparing political manifestos of multiple parties, policies, or agendas of different candidates or parties, should include minimum of 2 candidates.

        You must return only the category name (e.g., "Win Predictor") and nothing else.
        """

        # Input prompt from user
        user_input = request.GET.get('prompt')

        # Make the API request to Agent 1 (classifier)
        classification_response = client.chat.completions.create(
            model="model-identifier",
            messages=[
                {"role": "system", "content": system_prompt_agent1},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )

        # Get the classification result
        classification_result = classification_response.choices[0].message.content.strip()

        # Print the classification result
        print(f"Classification: {classification_result}")

        ###################################################################################################

        # Check if the classification is "Manifesto Comparator"
        if "Manifesto Comparator" in classification_result:
            chaining_for_manifesto.compare(user_input, client)
            
            # Load the outputs.json file
            file_path = 'comparison_output.json'

            with open(file_path, 'r') as file:
                answers = json.load(file)

            print("answers")
            print(answers)

            extracted_json = extract_json_from_string(answers)
            
            # Add 'Manifesto' category to the beginning of the JSON
            extracted_json_with_category = {"category": "Manifesto", "data": extracted_json}

            print("new function")
            print(extracted_json_with_category)
            
            return JsonResponse(extracted_json_with_category)


            
        elif "Semantic Analysis" in classification_result:
            print ("Running Semantic Analysis")
            # Example Usage
            data = """
            Anura Kumara Dissanayake: Positive 50%, Negative 30%, Neutral 20%.
            Ranil Wickremesinghe: Positive 40%, Negative 40%, Neutral 20%.
            Sajith Premadasa: Positive 45%, Negative 35%, Neutral 20%.
            Namal Rajapaksha: Positive 60%, Negative 20%, Neutral 20%.
            """

            chaining_sentiment.sentiment_analysis("data to be used" + data + " user input: " + user_input, client)
            
            # Load the outputs.json file
            file_path = 'sentiment_analysis_output.json'

            with open(file_path, 'r') as file:
                answers = json.load(file)
            print("answers")
            print(answers)
            extracted_json = extract_json_from_string(answers)
            print("new function")
            print(extracted_json)
            
            extracted_json_with_category = {"category": "Sentiment", "data": extracted_json}
            
            return JsonResponse(extracted_json_with_category)
        
        elif "Win Predictor" in classification_result:
            chaining_win_predictor.win_predictor(user_input, client)
            
        elif "Chat Bot" in classification_result:
            chaining_Chat_bot.chat_function(user_input, client)
            
            # Load the outputs.json file
            file_path = 'answer_output.json'

            with open(file_path, 'r') as file:
                answers = json.load(file)
            print("answers")
            print(answers)
            extracted_json = extract_json_from_string(answers)
            print("new function")
            print(extracted_json)
            
            extracted_json_with_category = {"category": "Chat", "data": extracted_json}
            
            return JsonResponse(extracted_json_with_category)

        else:
            print("The input does not require manifesto comparison.")
            

        
        return JsonResponse({'response': classification_result})
