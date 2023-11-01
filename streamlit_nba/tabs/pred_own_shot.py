# -*- coding: utf-8 -*-
"""
Created on Tue May 23 15:20:39 2023

@author: tmost
"""
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
import numpy as np
import joblib

sidebar_name = "Predict your own shot!"


def run():
    df = pd.read_csv('df.csv')
    dataset = df[['Period Grouped', 'Total Seconds Remaining', 'Shot Distance', 'Action Type Grouped', 'on_fire', 'Shot_Team', 'Shot Type', 'X Location', 'Y Location',
                  'Season Type', '2PT Field Goal_accuracy', '3PT Field Goal_accuracy', 'height', 'weight', 'age', 'W_PCT', 'Shot Made Flag']]


    st.title('Predict your own shot!')

    # Obtain player
    st.header('Player selection')
    top20_list = ['Chris Paul', 'Dirk Nowitzki', 'Kevin Durant', 'Pau Gasol',
           'LeBron James', 'Carmelo Anthony', 'Dwyane Wade', 'Dwight Howard',
           'Russell Westbrook', 'Kevin Love', 'Brook Lopez', 'James Harden',
           'Stephen Curry', 'Blake Griffin', 'DeMarcus Cousins',
           'Kyrie Irving', 'Anthony Davis', 'Damian Lillard',
           'Karl-Anthony Towns', 'Joel Embiid']
    player_selected = st.selectbox('Select the shooting player from the list of the 20 best players',
                                   options = top20_list)

    # Obtain information of the player
    player_info = df[['Player Name', 'height', 'weight', '2PT Field Goal_accuracy','3PT Field Goal_accuracy']]
    player_info = player_info.groupby('Player Name').mean()
    player_row = player_info[player_info.index == player_selected]
    height = player_row['height'].values[0]
    weight = player_row['weight'].values[0]
    two_pt_accuracy = player_row['2PT Field Goal_accuracy'].values[0]
    three_pt_accuracy = player_row['3PT Field Goal_accuracy'].values[0]

    # Obtain the period
    st.header('Period')
    periods = ['1', '2', '3', '4', 'OT']
    period = st.selectbox('Select period when the shot occurs', options = periods)

    # Obtain remaining time
    st.header('Remaining time of the period')
    minutes = st.number_input('Minutes', min_value=0, max_value=11, step=1)
    seconds = st.number_input('Seconds', min_value=0, max_value=59, step=1)
    total_seconds = minutes*60+seconds

    # Obtain Season Type
    st.header('Season Type')
    seasons = ['Regular Season', 'Playoffs']
    season = st.selectbox('Select period when the shot occurs', options = seasons)

    # Obtain shooting team
    st.header('Shooting Team')
    teams = ['Home', 'Away']
    team = st.selectbox('Select if the shooting team plays at home or away', options = teams)

    # Obtain shot location, shot distance and shot type
    st.header('Shot Location')
    st.write('Click on the court to select where the shot takes place')
    value = streamlit_image_coordinates("a_re.png", key="local")
    x_location = 0
    y_location = 0 
    if value is not None:
        x_location = (value["x"] - 250) / 10
        y_location = (-(value["y"] - 423) / 10)
        shot_distance = np.sqrt(x_location ** 2 + y_location ** 2).round(2)
    else:
        shot_distance = 0.0    
    if shot_distance > 24:
        type_shot = '3PT Field Goal'
    elif shot_distance > 22 and (x_location>22 or y_location<-22):
        type_shot = '3PT Field Goal'
    else:
        type_shot = '2PT Field Goal'
    st.write('You have selected a', type_shot,' with a distance of', shot_distance, 'to the basket')
    st.write('The position (X, Y) of the shot corresponds to', (x_location, y_location))

    # Obtain Action type
    st.header('Action Type')
    actions = df['Action Type'].value_counts().head(10).index
    action_i = st.selectbox('Select the action type of the shot', options = actions)
    action = df.groupby('Action Type')['Shot Made Flag'].agg(['mean', 'count']).reset_index().rename(columns={'mean' : 'accuracy'})
    a = action.loc[action['Action Type'] == action_i]
    bins = [0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    labels = ['action_below_40%', 'action_40-50%', 'action_50-60%', 'action_60-70%', 'action_70-80%', 'action_80-90%', 'action_above_90%']
    action_grouped = pd.cut(a['accuracy'], bins=bins, labels = labels)

    # Player on fire or not
    st.header('On Fire')
    fires = ['Yes', 'No']
    fire = st.selectbox('Select if the shooting player is on fire', options = fires)
    fire = 1 if fire == 'Yes' else 0

    # Generate the shot data
    shot = pd.DataFrame({
        'Period Grouped': period,
        'Total Seconds Remaining': total_seconds,
        'Shot Distance': shot_distance,
        'Action Type Grouped': action_grouped,
        'on_fire': fire,
        'Shot_Team': team,
        'Shot Type': type_shot,
        'X Location': x_location,
        'Y Location': y_location,
        'Season Type': season,
        '2PT Field Goal_accuracy': two_pt_accuracy,
        '3PT Field Goal_accuracy': three_pt_accuracy,
        'height': height,
        'weight': weight,
        'age': 27,
        'W_PCT': 50   
    })

    # Import models and scalers. I only present the examples of Lebron and Curry
    import pickle
    if 'player_selected' == 'LeBron James': 
        model = pickle.load(open('lebron_model.sav', 'rb'))
        scaler = pickle.load(open('scaler_lebron.pkl', 'rb'))
    else:
        model = pickle.load(open('curry_model.sav', 'rb'))
        scaler = pickle.load(open('scaler_curry.pkl', 'rb'))

    shot_i = pd.concat([dataset, shot], ignore_index=True)

    shot_i = shot_i.drop(['2PT Field Goal_accuracy', '3PT Field Goal_accuracy', 'height', 'weight', 'Shot Made Flag'], axis=1)

    categorical_cols = shot_i.select_dtypes(include=['object', 'category']).columns
    shot_i = pd.get_dummies(shot_i, columns=categorical_cols)
    numeric_cols = shot_i.select_dtypes(include=['float64', 'int64']).columns
    shot_i[numeric_cols] = scaler.transform(shot_i[numeric_cols])

    #Perform prediction
    y_pred = model.predict(shot_i.tail(1))
    proba = model.predict_proba(shot_i.tail(1))
    y_pred = 'missed' if y_pred == 0 else 'made'
    if y_pred == 'missed':
        st.markdown('<p style="font-size: 24px;">The result of the shot is <span style="color: red;">{}</span></p>'.format(y_pred), unsafe_allow_html=True)
    elif y_pred == 'made':
        st.markdown('<p style="font-size: 24px;">The result of the shot is <span style="color: green;">{}</span></p>'.format(y_pred), unsafe_allow_html=True)

    st.write('With a probability of', proba.max())