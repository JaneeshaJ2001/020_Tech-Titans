from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

# Fixed database path for Sajith
CHROMA_PATH = "sajith_data"

PROMPT_TEMPLATE = """
Answer based only on the following context:

{context}

---

Provide an answer based on the above context: {question}

Obey following rules:
- Ignore the names in the question, for example, if it asks about Sajith's economy. Just answer about economy.
- Answer like a human.
- Don't include parts like "based on the provided context" in the answer.
"""

def query_rag_local(prompt: str):
    # Print the input query
    print("Querying RAG with:", prompt)

    # Prepare the embedding function and load Sajith's database.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
    print("CHROMA_PATH:", CHROMA_PATH)

    # Search the database for relevant context.
    results = db.similarity_search_with_score(prompt, k=5)

    # Prepare the context text from the results.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Create the prompt using the context and the query.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt_template.format(context=context_text, question=prompt)
    
    print("Generated Prompt:", formatted_prompt)

    # Use the model to generate the response.
    model = Ollama(model="llama3.1")
    response_text = model.invoke(formatted_prompt)

    # Extract sources for reference.
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = {
        "response": response_text,
        "sources": sources
    }

    return formatted_response

if __name__ == "__main__":
    # Define your prompt directly here.
    prompt = "What are Sajith's economic policies?"

    # Query the RAG system with the defined prompt.
    response = query_rag_local(prompt)
    
    # Print the formatted response
    print("Response:", response["response"])
    print("Sources:", response["sources"])
