import argparse
from flask import Flask, request, jsonify
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

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

COMPARISON_PROMPT_TEMPLATE = """
Compare {candidate_1} and {candidate_2} on the following field: {field}. Provide 10 points of comparison for each candidate. Keep the comparison clear and concise:

{context}

---

List the comparison points for {candidate_1} and {candidate_2} regarding {field}:
"""

app = Flask(__name__)

def get_candidate_db_path(candidate_name):
    # Construct the candidate-specific database path
    if "sajith" in candidate_name.lower():
        return f"sajith_data"
    elif "anura" in candidate_name.lower():
        return f"anura_data"
    elif "ranil" in candidate_name.lower():
        return f"ranil_data"
    else:
        return f"common_data"

@app.route('/query', methods=['GET'])
def query_rag():
    query_text = request.args.get("query_text")

    if not query_text:
        return jsonify({"error": "No query_text provided"}), 400
    
    # Replace % with spaces in query_text
    query_text = query_text.replace("%", " ")
    
    print("Querying RAG with:", query_text)

    # Determine the appropriate database path
    if "sajith" in query_text.lower():
        CHROMA_PATH = "sajith_data"
    elif "anura" in query_text.lower():
        CHROMA_PATH = "anura_data"
    elif "ranil" in query_text.lower():
        CHROMA_PATH = "ranil_data"
    else:
        CHROMA_PATH = "common_data"
        
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
    print("CHROMA_PATH:", CHROMA_PATH)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    print(prompt)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = {
        "response": response_text,
        "sources": sources
    }

    return jsonify(formatted_response)

@app.route('/compare', methods=['GET'])
def compare():
    # Get the input parameters
    candidate_1 = request.args.get("candidate_1")
    candidate_2 = request.args.get("candidate_2")
    field = request.args.get("field")
    
    if not candidate_1 or not candidate_2 or not field:
        return jsonify({"error": "Please provide candidate_1, candidate_2, and field to compare."}), 400

    # Fetch the database path for each candidate
    candidate_1_db_path = get_candidate_db_path(candidate_1)
    candidate_2_db_path = get_candidate_db_path(candidate_2)

    # Prepare the embedding function
    embedding_function = get_embedding_function()

    # Prepare the DBs for each candidate
    db_1 = Chroma(persist_directory=candidate_1_db_path, embedding_function=embedding_function)
    db_2 = Chroma(persist_directory=candidate_2_db_path, embedding_function=embedding_function)

    # Fetch context for both candidates
    query_text_1 = f"{candidate_1} {field}"
    query_text_2 = f"{candidate_2} {field}"

    results_1 = db_1.similarity_search_with_score(query_text_1, k=5)
    results_2 = db_2.similarity_search_with_score(query_text_2, k=5)
    
    print("Results for candidate 1:", results_1)
    print("Results for candidate 2:", results_2)

    context_text_1 = "\n\n---\n\n".join([doc.page_content for doc, _score in results_1])
    context_text_2 = "\n\n---\n\n".join([doc.page_content for doc, _score in results_2])

    context_text = f"Context for {candidate_1}:\n{context_text_1}\n\n---\n\nContext for {candidate_2}:\n{context_text_2}"

    # Generate the comparison prompt
    prompt_template = ChatPromptTemplate.from_template(COMPARISON_PROMPT_TEMPLATE)
    prompt = prompt_template.format(candidate_1=candidate_1, candidate_2=candidate_2, field=field, context=context_text)
    
    print("Comparison Prompt:", prompt)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    formatted_response = {
        "response": response_text,
        "candidate_1": candidate_1,
        "candidate_2": candidate_2,
        "field": field
    }

    return jsonify(formatted_response)


def run_cli():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    response = query_rag_local(query_text)
    print(response)


def query_rag_local(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=2)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return formatted_response


if __name__ == "__main__":
    # Choose whether to run the Flask server or the CLI
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        run_cli()
    else:
        # Run the Flask server on all network interfaces
        app.run(host='0.0.0.0', port=8000, debug=True)
