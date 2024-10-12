from langchain.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function

# Function to dynamically select Chroma path based on input name.
def select_chroma_path(person_name: str) -> str:
    # Map the person name to the respective database path.
    chroma_map = {
        "sajith": "sajith_data",
        "anura": "anura_data",
        "ranil": "ranil_data"
    }
    
    # Normalize the input name and return the corresponding path.
    normalized_name = person_name.lower().strip()
    return chroma_map.get(normalized_name, "default_data")  # Default if no match found

# Function to query the vector database and return the top 5 most similar documents.
def query_rag_local(person_name: str, prompt: str):
    # Print the input query and the selected person.
    print(f"Querying vector database for {person_name} with prompt:", prompt)
    
    # Dynamically select the Chroma database path based on the person's name.
    CHROMA_PATH = select_chroma_path(person_name)
    print(f"Selected CHROMA_PATH: {CHROMA_PATH}")

    # Prepare the embedding function and load the respective database.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the database for relevant context (top 5 results).
    results = db.similarity_search_with_score(prompt, k=5)

    # Print the top 5 most similar documents
    print("\nTop 5 Similar Documents:")
    for i, (doc, score) in enumerate(results):
        print(f"{i+1}. Document ID: {doc.metadata.get('id')}, Score: {score}")
        print(f"Content: {doc.page_content}\n")

if __name__ == "__main__":
    # Prompt for user input of person name.
    person_name = input("Enter the person's name (Sajith, Anura, Ranil): ").strip()

    # Define your question prompt directly here.
    prompt = "What are their economic policies?"

    # Query the vector database with the selected person's name and the defined prompt.
    query_rag_local(person_name, prompt)
