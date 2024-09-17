import streamlit as st
import random
import time

def manifesto_comparator_page():
    st.title("Manifesto Comparator")

    col1, col2 = st.columns(2)

    with col1:
        option1 = st.selectbox(
            "Candidate 1 name",
            ("Anura Kumara Dissanayake", "Sajith Premadasa", "Ranil Wickramasinghe", "Namal Rajapaksa"),
            index=None,
            placeholder="Select ...",
        )

    with col2:
        option2 = st.selectbox(
            "Candidate 2 name",
            ("Anura Kumara Dissanayake", "Sajith Premadasa", "Ranil Wickramasinghe", "Namal Rajapaksa"),
            index=None,
            placeholder="Select ...",
        )
    


    
    
    
    