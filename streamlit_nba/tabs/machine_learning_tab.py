import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

location = 'C:\\Users\\w_sat\\Desktop\\Python\\Projet_NBA\\streamlit_nba\\'

# Chargement des modèles

models_general = {
    "Gradient Boosting Classifier": joblib.load(f'{location}gradient_boosting_classifier.joblib'),
    "Logistic Regression": joblib.load('gridcv_lr.joblib'),
    "LightGBM": joblib.load('light_gbm.joblib'),
    "Random Forest": joblib.load('random_forest_model.joblib'),
    "XGBoost": joblib.load('XGBoost.joblib')
}

models_single_player = {
    "XGBoost (Curry)": joblib.load('XGBoost_Curry.joblib'),
    "XGBoost (James)": joblib.load('XGBoost_James.joblib')
}

# Dictionnaire des accuracies pour chaque modèle
accuracies = {
    "Gradient Boosting Classifier": 0.6356701550876308,
    "Logistic Regression": 0.6286933131593325,
    "LightGBM": 0.6426259824318077,
    "Random Forest": 0.6244903963350565,
    "XGBoost": 0.6408397427814904,
    "XGBoost (Curry)": 0.6704204204204204,
    "XGBoost (James)": 0.686372269705603
}

# Classification reports pour chaque modèle

classification_reports = {
    "Logistic Regression": 
    {"0": {"Precision": 0.61, "Recall": 0.71, "F1-score": 0.66, "Support": 23692},
     "1": {"Precision": 0.66, "Recall": 0.55, "F1-score": 0.60, "Support": 23894}},
     
    "Random Forest": 
    {"0": {"Precision": 0.61, "Recall": 0.68, "F1-score": 0.64, "Support": 23692},
     "1": {"Precision": 0.64, "Recall": 0.57, "F1-score": 0.60, "Support": 23894}},
     
    "Gradient Boosting Classifier": 
    {"0": {"Precision": 0.61, "Recall": 0.75, "F1-score": 0.67, "Support": 23692},
     "1": {"Precision": 0.68, "Recall": 0.52, "F1-score": 0.59, "Support": 23894}},
     
    "LightGBM": 
    {"0": {"Precision": 0.62, "Recall": 0.75, "F1-score": 0.68, "Support": 23692},
     "1": {"Precision": 0.68, "Recall": 0.54, "F1-score": 0.60, "Support": 23894}},
     
    "XGBoost": 
    {"0": {"Precision": 0.61, "Recall": 0.75, "F1-score": 0.67, "Support": 23692},
     "1": {"Precision": 0.68, "Recall": 0.54, "F1-score": 0.60, "Support": 23894}},
     
    "XGBoost (Curry)": 
    {"0": {"Precision": 0.67, "Recall": 0.66, "F1-score": 0.67, "Support": 1329},
     "1": {"Precision": 0.67, "Recall": 0.68, "F1-score": 0.67, "Support": 1335}},
     
    "XGBoost (James)": 
    {"0": {"Precision": 0.65, "Recall": 0.81, "F1-score": 0.72, "Support": 2108},
     "1": {"Precision": 0.75, "Recall": 0.56, "F1-score": 0.64, "Support": 2104}}
}


# Matrices de confusion pour chaque modèle
confusion_matrices = {
    "Gradient Boosting Classifier": [[16858, 6834], [10835, 13059]],
    "Logistic Regression": [[16178, 7514], [10355, 13539]],
    "LightGBM": [[17764, 5928], [11409, 12485]],
    "Random Forest": [[17697, 5995], [11011, 12883]],
    "XGBoost": [[17675, 6017], [11074, 12820]],
    "XGBoost (Curry)": [[878, 451], [427, 908]],
    "XGBoost (James)": [[1703, 405], [916, 1188]]
}

sidebar_name = "Machine Learning"

def run():
    st.title('Machine Learning')

    st.write("## Pre-processing")
    st.write("""- Separated dataset into features (X) and target (‘Shot Made Flag’).
- Balanced data using the 'RandomUnderSampler' for equal successful and missed shots.
- Split data into a training set (80%) and a test set (20%) with 'train_test_split'.
- Encoded categorical variables using 'get_dummies'.
- Standardized continuous numerical variables using 'StandardScaler' to handle differences in magnitudes.
""")

    st.write("## Training the models")
    st.write("""- Chose first logistic regression for this binary classification problem due to its ease of implementation and speed.
- Initial model without adjusted hyperparameters yielded an accuracy of 0.628.
- Optimized hyperparameters using cross-validation with a search grid (GridSearchCV), improving accuracy to 0.631.
- Tried to implement other models such as: RandomForest, Gradient Boosting Classifier, LGBM, XGBoost.
- Gradient boosting models achieved the highest accuracy, reaching over 64%.
""")


 # Choix du modèle général
    st.write("## Models trained on the top 20 players in the NBA")
    model_name_general = st.selectbox("Select your model",list(models_general.keys()))
    model_general = models_general[model_name_general]
    st.write(f"## Model: {model_name_general}")
    st.write("### Model Parameters")
    st.write(model_general.get_params())
    st.write("### Accuracy")
    st.write(f"**{accuracies[model_name_general]*100:.2f}%**")
    st.write("### Classification Report")
    st.table(classification_reports[model_name_general])
    # Matrice de confusion
    st.write("### Confusion Matrix")
    confusion_matrix_general = confusion_matrices[model_name_general]
    fig, ax = plt.subplots(figsize=(10,7))
    sns.heatmap(confusion_matrix_general, annot=True, fmt='d', cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    #  Features importance
    if model_name_general == "Gradient Boosting Classifier":
        st.write("### Features importance")
        st.image("gradient_boosting_features.png", caption="Top features for Gradient Boosting Classifier", use_column_width=True, output_format='auto')
    if model_name_general == "XGBoost" :
        st.write("### Features importance")
        st.image("XGboost_features.png", caption="Top features for XGBoost", use_column_width=True, output_format='auto')
   
    


    # Choix du modèle pour un joueur unique

    st.write("## Model trained on a single players")
    model_name_single_player = st.selectbox("Select your model", list(models_single_player.keys()))
    model_single_player = models_single_player[model_name_single_player]
    st.write(f"## Model: {model_name_single_player}")
    st.write("### Model Parameters")
    st.write(model_single_player.get_params())
    st.write("### Accuracy")
    st.write(f"**{accuracies[model_name_single_player]*100:.2f}%**")
    st.write("### Classification Report")
    st.table(classification_reports[model_name_single_player])
    # Matrice de confusion
    st.write("### Confusion Matrix")
    confusion_matrix_single_player = confusion_matrices[model_name_single_player]
    fig, ax = plt.subplots(figsize=(10,7))
    sns.heatmap(confusion_matrix_single_player, annot=True, fmt='d', cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    # Features importance
    st.write("### Features importance")
    st.image("XGboost_features.png", caption="Top features for XGBoost", use_column_width=True, output_format='auto')
    
    
     # Graphique de comparaison des diff modèles

    st.write("## Model Accuracy Comparison")
    model_accuracies = {
    'Logistic Regression': 62.87,
    'Random Forest Classifier': 62.45,
    'Gradient Boosting Classifier': 63.57,
    'XGBoost Classifier': 64.08,
    'LGBM Classifier': 64.26,
    'XGB Curry Model': 67.04,
    'XGB James Model': 68.64}

    fig, ax = plt.subplots(figsize=(8, 6))

    colors = ['blue' if (model!='XGB Curry Model' and model!='XGB James Model') else 'red' for model in model_accuracies.keys()]
    plt.bar(model_accuracies.keys(), model_accuracies.values(), color=colors)
    plt.title('Model Accuracy Comparison')
    plt.xlabel('Model')
    plt.ylabel('Accuracy (%)')
    plt.xticks(rotation=45)
    plt.ylim([60, 70])
    st.pyplot(plt.gcf())


    st.write("""- We can observe that the single player models provide a much more satisfying accuracy, almost reaching 69%. 
- It is therefore highly advisable to exceed 70% accuracy with unique player models by adding new variables 
         and implementing other optimizations.
        """)
    st.write("\n\n\n\n\n\n\n\n\n")
   


    


    

