import streamlit as st
import base64

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode() 
    
def set_background(image_file):
    base64_image = get_base64(image_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: 100% 100%;  /* Makes the background scale dynamically */
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def home():
    #set_background("candidates.jpg")
    
    st.title("Who will win the Presidential Election ?")
    

if __name__ == '__main__':
    home()
