import streamlit as st
import requests
import time

# Streamed response emulator to simulate typing effect
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def electobot_page():
    # Page title
    st.markdown(
        """
        <h1 style='text-align: center; color: #FF6347;'>Electobot - Your Election Q&A Companion</h1>
        <p style='text-align: center;'>Ask questions about the presidential election candidates, their policies, and manifestos!</p>
        <hr style='border: 1px solid #FF6347;'>
        """, unsafe_allow_html=True
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"<div style='color: #333;'>{message['content']}</div>", unsafe_allow_html=True)

    # Accept user input
    if prompt := st.chat_input("Ask about candidates, policies, or anything election-related..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in the chat container
        with st.chat_message("user"):
            st.markdown(f"<div style='color: #008080;'>{prompt}</div>", unsafe_allow_html=True)

        # Send the prompt to the local API
        try:
            response = requests.get(f"http://localhost:8000/query?query_text={prompt}")
            response_json = response.json()

            # Extract the response from the JSON response
            assistant_response = response_json.get("response", "Sorry, I couldn't retrieve a proper response.")

            # Display assistant's response with a typing effect
            with st.chat_message("assistant"):
                st.write_stream(response_generator(assistant_response))

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        except Exception as e:
            with st.chat_message("assistant"):
                st.markdown("<div style='color: red;'>Error occurred while connecting to the API.</div>", unsafe_allow_html=True)
