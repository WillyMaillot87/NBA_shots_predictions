import boto3
from decouple import config
import os

# To obtain access to the S3 bucket where the files are stored, please contact me at the following address : w.maillot@gmail.com

# Répertoire de destination des datasets
data_dir = 'data/'

# Liste des fichiers à télécharger
datasets_to_download = [
    'Seasons_Stats.csv',
    'player_data.csv',
    'NBA Shot Locations 1997 - 2020.csv',
    'ranking.csv',
    'teams.csv'
]

# Préparation de la connexion au Bucket S3 d'Amazon AWS
s3_client = boto3.client('s3', region_name=config('AWS_S3_REGION'), aws_access_key_id=config('AWS_USER_KEY_ID'), aws_secret_access_key=config('AWS_USER_KEY'))

# Télécharger les fichiers uniquement s'ils ne sont pas déjà présents dans le répertoire "data"
for file_name in datasets_to_download:
    local_path = os.path.join(data_dir, file_name)

    # Vérifier si le fichier existe déjà
    if not os.path.exists(local_path):
        print(f"Téléchargement de {file_name}...")
        s3_client.download_file(Bucket=config('AWS_S3_BUCKET_NAME'), Key=file_name, Filename=local_path)
        print(f"{file_name} téléchargé avec succès.")
    else:
        print(f"{file_name} est déjà présent dans le répertoire.")

print("Le téléchargement des datasets est terminé.")

print("Téléchargement des modèles pour streamlit...")

# Répertoire de destination des datasets
streamlit_dir = 'streamlit_app/'

streamlit_files_to_download = [
    'XGBoost_James.joblib',
    'XGBoost_Curry.joblib',
    'XGBoost.joblib',
    'scaler_lebron.pkl',
    'scaler_curry.pkl',
    'random_forest_model.joblib',
    'light_gbm.joblib',
    'curry_model.sav',
    'lebron_model.sav',
    'gridcv_lr.joblib',
    'gradient_boosting_classifier.joblib',
    'df.csv',
    'df1.csv',
    'working_dataframe.csv',
    'Seasons_Stats.csv',
    'player_data.csv',
    'NBA Shot Locations 1997 - 2020.csv',
    'ranking.csv',
    'teams.csv'
]

# Télécharger les fichiers uniquement s'ils ne sont pas déjà présents dans le répertoire "data"
for file_name in streamlit_files_to_download :
    local_path = os.path.join(models_dir, file_name)

    # Vérifier si le fichier existe déjà
    if not os.path.exists(local_path):
        print(f"Téléchargement de {file_name}...")
        s3_client.download_file(Bucket=config('AWS_S3_BUCKET_NAME'), Key=file_name, Filename=local_path)
        print(f"{file_name} téléchargé avec succès.")
    else:
        print(f"{file_name} est déjà présent dans le répertoire.")

print("Le téléchargement des datasets est terminé.")