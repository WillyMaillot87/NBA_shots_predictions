import streamlit as st


title = 'Conclusion'
sidebar_name = "Conclusions"


    
    
def run():
    
    
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    
    st.subheader('Conclusions:')

    
    st.write("""- An XGBoost-type model has been trained and obtains an accuracy above 64% to predict the shooting performance of the top 20 NBA players.
- The accuracy can be improved if an individual model is trained for each player, where almost 69% accuracy was achieved for a player like LeBron James.
- The models show an overestimation in the prediction of missed shots. This is because the variable 'Shot Distance' and 'Action Type' take a lot of importance for the model. Therefore, the farther the shot is or the more complicated the action, the more the model will always tend to classify it as a miss.
- This overestimation is balanced when we classify shots of players with a good percentage of long distance shots, such as Stephen Curry.
- We have developed variables through feature engineering such as 'On-Fire' that have helped the model make decisions in certain situations.
- In order to further increase the accuracy of the models, it is important to be able to use some variables such as defensive pressure, assist quality, etc. that are not currently available in the databases.
""")