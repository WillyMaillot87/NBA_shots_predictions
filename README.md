NBA Shots Prediction
==============================

The main objective of this project is the prediction of shooting performances of NBA players.

Project Organization
------------
    
    ├── data
    ├── download_data.py
    ├── LICENSE
    ├── Notebooks
    │   ├── Dataframe generation and preparation.ipynb
    │   ├── Exploratory Data Analysis.ipynb
    │   └── Models Training.ipynb
    ├── README.md
    ├── References
    │   └── Rapport Final.docx
    ├── requirements.txt
    ├── streamlit_nba
    │   ├── app.py
    │   ├── a_re.png
    │   ├── assets
    │   ├── Ballon.png
    │   ├── github-mark.png
    │   ├── github-mark-white.png
    │   ├── gradient_boosting_features.png
    │   ├── Image panier.png
    │   ├── __pycache__
    │   │   ├── config.cpython-310.pyc
    │   │   └── member.cpython-310.pyc
    │   ├── style.css
    │   ├── tabs
    │   │   ├── conclusions.py
    │   │   ├── credits.py
    │   │   ├── Exploratory_data_analysis.py
    │   │   ├── intro.py
    │   │   ├── machine_learning_tab.py
    │   │   ├── pred_own_shot.py
    │   └── XGboost_features.png

------------

About this project
------------

This project focuses on analyzing the shooting performance of players in the National Basketball Association (NBA) using data on shots taken between 1997 and 2020. The main objective is to develop a classification model to predict the probability of a shot being successful. The data includes information such as the location of shots on the court, variables related to shooting actions, and other player characteristics.

The team used various models, including XGBoost, to train the prediction model. The analysis reveals that the model shows variable accuracy depending on the shot class, with better performance in predicting missed shots. The importance of variables, such as action type and shot distance, was examined to interpret the results.

Improvement perspectives were explored, including training individual models for each player, which showed an increase in accuracy. The addition of new variables, such as defender distance and ball possession time, was also considered to enhance the model's performance. Despite challenges related to data availability and computing power constraints, the project resulted in a model capable of reasonably accurately predicting made and missed shots, providing valuable insights into factors influencing outcomes in professional basketball.

We invite you to read the entire report (References/Rapport Final.docx) for more details.

------------

How to use it ?
------------

**1 - set the environment**

- Clone the repository

- Create a virtual environement by running the following command :

    `virutalenv venv`

    `source venv/bin/activate`

    `pip install -m requirements.txt`

**2 - Download the data**

**First solution : download from the script**

To automatically download all the datasets and the models you will need to get an access token. Please contact @willymaillot87.

Once you get the token execute the script ***'download_data.py'***

**Second Solution : manually download the datasets and create the models**

Download all the necessary CSVs from the following links to the folder ***'data'***. You may need to create an account to kaggle to download those datasets :
- 'Seasons_Stats.csv' : https://www.kaggle.com/datasets/drgilermo/nba-players-stats?select=Seasons_Stats.csv
- 'player_data.csv' : https://www.kaggle.com/datasets/drgilermo/nba-players-stats?select=player_data.csv
- 'NBA Shot Locations 1997 - 2020.csv' : https://www.kaggle.com/datasets/jonathangmwl/nba-shot-locations?resource=download
- 'teams.csv' : https://www.kaggle.com/datasets/nathanlauga/nba-games?select=teams.csv

Once you get the datasets just run all the cells from the notebooks: 
1. 'Notebooks/Dataframe generation and preparation.ipynb'
2. 'Notebooks/Models Training.ipynb'

**3 - Run the streamlit app**

- In order to access to the streamlit app please run the following commands :

    `cd streamlit_app`

    `streamlit run app.py`

- Open your browser to this adress :
    
    *localhost:8501*