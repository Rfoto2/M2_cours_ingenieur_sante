import numpy as np
from clinical_cool_etud.config import DATA_DIR

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():

    dataframe_clinical_data = pd.read_csv(DATA_DIR / "clinical_data_pbc.csv")

    print(dataframe_clinical_data.head())

    # copie du dataset
    dataframe_clinical_data_copy = dataframe_clinical_data.copy()

    n_rows = len(dataframe_clinical_data_copy)
    n_patients = dataframe_clinical_data_copy['id'].nunique()
    print(f"Nombre total d'observations (visites) : {n_rows}")
    print(f"Nombre de patients uniques : {n_patients}")
    print(f"Moyenne de visites par patient : {n_rows / n_patients:.2f}")

    # Visualiser la distribution du nombre de visites par patient

    # Calcul du % de manquants par colonne

    # Matrice de Corrélation (attention, données longitudinales !)


    # Visualiser la distribution des temps de survie

    # Distribution des évènements (death, transplant, censor)

if __name__ == "__main__":
    main()





