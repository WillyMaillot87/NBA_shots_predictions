import streamlit as st
from PIL import Image
import pandas as pd



sidebar_name = "Home"


def run():
    # Image loading 
    image_path = "Image panier.png"
    image = Image.open(image_path)
    # Image display
    st.image(image)
    # Title display (overlaid on image)
    st.markdown("<h1 style='position: relative; top: 50%; left: 50%; transform: translate(-48%, -148%); color: white;'>Analysis of NBA players' shots</h1>", unsafe_allow_html=True)   
    
    
    
    # Project introductory text
    st.subheader("The Project") 
    st.markdown('''For several years now, data has been advancing hand in hand with the NBA, 
continuously striving for greater performance and this, by focusing on different 
aspects of the game.

Every action and even non-action (such as rest, for example) is studied, analyzed, 
dissected to reach the pinnacle of performance.
With a minimum of 82 matches per team each year, we are talking about millions of 
actions to examine over time.
Whether it's rebounds, interceptions, assists, a player's ability to change a game,
or of course, shots, everything is scrutinized through data analysis.

Our project is aligned within this context. Indeed, this project aims to utilize 
NBA data to determine the probability of a shot being successful or not.''')

    
