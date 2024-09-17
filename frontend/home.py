import streamlit as st
import base64

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode() 


def set_bg_from_local(image_file):
    bin_str = get_base64(image_file)
    st.markdown(
        f"""
        <style>
        .stAppViewContainer {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
        }}
        [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}
        </style>
        """,
        unsafe_allow_html=True
    )


def home():
    
    set_bg_from_local('imgs/candidates1.png')
    st.title("Who will be the Next President?")
    


if __name__ == '__main__':
    home()
