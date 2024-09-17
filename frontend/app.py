import streamlit as st
from streamlit_option_menu import option_menu
from sentiment_analysis import sentiment_analysis_page
from electobot import electobot_page
from manifesto_comparator import manifesto_comparator_page
from winPredictor import winPredictor
from home import home


def main():
    # Navigation bar
    st.set_page_config(page_title="SL President'24", layout="wide")
    

    with st.sidebar:
        selected = option_menu(
        "SL President\'24",  # Title of the menu
        ["Home", "Win Predictor", "Sentiment Analysis", "ElectoBot", "Manifesto Comparator"],  # Menu items
        icons=["house", "camera", "clipboard", "book", "book"],  # Icons for each item
        menu_icon="app-indicator",  # Icon for the menu header
        default_index=0,  # Default selected item
        styles={
            "container": {"padding": "5!important"},
            "icon": {"color": "orange", "font-size": "25px"},  # Color and size for the icons
            "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green", "color": "white"},
        }
    )    
    
    if selected == 'Home':  
        home()

        
    elif selected == 'Sentiment Analysis':
        sentiment_analysis_page()
            
        
    elif selected == 'ElectoBot':
        electobot_page()
        
    elif selected == 'Manifesto Comparator':
        manifesto_comparator_page()

    elif selected == 'Win Predictor':
        winPredictor()

if __name__ == '__main__':
    main()