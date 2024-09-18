import streamlit as st
import requests

# Function to handle the comparison and display history
def manifesto_comparator_page():
    st.title("Manifesto Comparator")

    # Predefined fields for comparison
    predefined_fields = [
        "Economy", "Education", "Healthcare", "Foreign Policy", 
        "Environment", "Defense", "Infrastructure", "Corruption", 
        "Human Rights", "Technology"
    ]

    # List of candidates and their parties
    candidates = {
        "Ranil Wickremesinghe (Independent)": "Ranil Wickremesinghe",
        "Sajith Premadasa (SJB)": "Sajith Premadasa",
        "Anura Kumara Dissanayake (NPP)": "Anura Kumara Dissanayake",
        "Namal Rajapaksa (SLPP)": "Namal Rajapaksa"
    }

    # Columns for candidate selection
    col1, col2 = st.columns(2)

    with col1:
        candidate_1 = st.selectbox("Candidate 1", list(candidates.keys()), index=0)

    with col2:
        candidate_2 = st.selectbox("Candidate 2", list(candidates.keys()), index=1)

    # Extract actual candidate names for the API request
    candidate_1_name = candidates[candidate_1]
    candidate_2_name = candidates[candidate_2]

    # Field comparison selection
    comparison_option = st.selectbox("Select a field to compare", predefined_fields, index=0)
    manual_field = st.text_input("Or enter a custom comparison field (optional)")

    # Use manual field if provided, else use predefined option
    field = manual_field if manual_field.strip() else comparison_option

    # History of comparisons (stored in session state)
    if "comparison_history" not in st.session_state:
        st.session_state.comparison_history = []

    if st.button("Compare"):
        if candidate_1_name and candidate_2_name and field:
            # Prepare the API URL with parameters
            url = f"http://localhost:8000/compare?candidate_1={candidate_1_name}&candidate_2={candidate_2_name}&field={field}"
            
            # Send a GET request to the API
            response = requests.get(url)
            
            if response.status_code == 200:
                # Get the response text
                comparison_result = response.json().get("response", "No comparison result found.")

                # Save comparison to history
                st.session_state.comparison_history.append({
                    "candidate_1": candidate_1_name,
                    "candidate_2": candidate_2_name,
                    "field": field,
                    "result": comparison_result
                })
            else:
                st.write("Error in fetching the comparison result. Please try again.")
        else:
            st.write("Please enter valid inputs for both candidates and the comparison field.")

    # Display the history of comparisons
    st.write("### Comparison History")
    for comparison in st.session_state.comparison_history:
        st.write(f"**{comparison['candidate_1']} vs {comparison['candidate_2']}** - Field: {comparison['field']}")
        st.write(comparison['result'])
        st.write("---")  # Separator for each comparison
