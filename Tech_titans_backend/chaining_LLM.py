from openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
import json
import chaining_for_manifesto
import chaining_Chat_bot
import chaining_sentiment
import chaining_win_predictor

# Point to the local server
client = OpenAI(base_url="http://192.168.137.1:1234/v1", api_key="lm-studio")

# System prompt for classification
system_prompt_agent1 = """
You are an election-related task classifier. For each prompt entered, you must categorize it into one of the following categories and return only the category name:

1. Chat Bot: If the input involves general conversation, Q&A, or interactive dialogue without a specific analysis or comparison task.
2. Semantic Analysis: If the input is related to social media content analysis.
3. Win Predictor: If the input is related to predicting election outcomes based on polling data, trends, or performance metrics.
4. Manifesto Comparator: If the input involves comparing political manifestos, policies, or agendas of different candidates or parties, should include minimum of 2 candidates.

You must return only the category name (e.g., "Win Predictor") and nothing else.
"""

# Input prompt from user
user_input = "why Ranil is so important for the economy"

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
    
elif "Semantic Analysis" in classification_result:
    chaining_sentiment.sentiment_analysis(user_input, client)
    
elif "Win Predictor" in classification_result:
    chaining_win_predictor.win_predictor(user_input, client)
    
elif "Chat Bot" in classification_result:
    chaining_Chat_bot.chat_function(user_input, client)

else:
    print("The input does not require manifesto comparison.")
    
