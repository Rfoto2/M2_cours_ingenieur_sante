import numpy as np
#from clinical_cool_etud.config import DATA_DIR
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
    plt.figure(figsize=(8, 4))
    visites_par_patient = dataframe_clinical_data_copy.groupby('id').size()
    sns.histplot(visites_par_patient, bins=range(1, 20), discrete=True, color='teal')
    plt.title("Distribution du nombre de visites par patient")
    plt.xlabel("Nombre de visites")
    plt.ylabel("Nombre de patients")
    plt.savefig(DATA_DIR / "distribution_visites_par_patient.png")
    plt.close()


    print("\n--- ANALYSE DES DONNÉES MANQUANTES ---")

    # Calcul du % de manquants par colonne
    missing_percent = dataframe_clinical_data_copy.isnull().mean() * 100
    missing_percent = missing_percent[missing_percent > 0].sort_values(ascending=False)

    if not missing_percent.empty:
        plt.figure(figsize=(10, 8))
        sns.barplot(x=missing_percent.index, y=missing_percent.values)
        plt.title("Pourcentage de données manquantes par variable")
        plt.ylabel("% Manquant")
        plt.xticks(rotation=45)
        plt.savefig(DATA_DIR / "pourcentage_manquants.png")
        plt.close()
    else:
        print("Ce jeu de données ne contient pas de Nan.")
        plt.figure(figsize=(10, 8))
        sns.barplot(x=missing_percent.index, y=missing_percent.values)
        plt.title("Pourcentage de données manquantes par variable")
        plt.ylabel("% Manquant")
        plt.xticks(rotation=45)
        plt.savefig(DATA_DIR / "pourcentage_manquants.png")
        plt.close()

    print("\n--- DISTRIBUTIONS ET OUTLIERS ---")

    # Variables clés du foie
    vars_to_check = ['serBilir', 'serChol', 'albumin', 'alkaline', 'SGOT', 'platelets', 'prothrombin', 'histologic']

    # Filtrer pour s'assurer que les colonnes existent
    vars_existing = [v for v in vars_to_check if v in dataframe_clinical_data_copy.columns]

    for var in vars_existing:
        plt.figure(figsize=(12, 4))

        # Distribution brute
        plt.subplot(1, 2, 1)
        sns.histplot(dataframe_clinical_data_copy[var], kde=True, color='skyblue')
        plt.title(f"Distribution Brute : {var}")

        #  Distribution Log (si valeurs > 0)
        if dataframe_clinical_data_copy[var].min() > 0:
            plt.subplot(1, 2, 2)
            sns.histplot(np.log1p(dataframe_clinical_data_copy[var]), kde=True, color='purple')
            plt.title(f"Distribution Log({var})")
            plt.savefig(DATA_DIR / f"distribution_{var}.png")
            plt.close()

    print("\n--- MATRICE DE CORRÉLATION ---")

    # On ne prend que les colonnes numériques
    numeric_df = dataframe_clinical_data_copy.select_dtypes(include=[np.number])

    # Attention : En longitudinal, calculer la corrélation sur toutes les lignes
    # surpondère les patients qui ont beaucoup de visites.
    corr_matrix = numeric_df.groupby('id').mean().corr()

    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Masquer la partie haute
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title("Matrice de Corrélation (Moyennée par patient)")
    plt.savefig(DATA_DIR / "matrice_correlation.png")
    plt.close()

    # ANALYSE DES TEMPS INTER-VISITES 

    print("\n--- ANALYSE DES TEMPS INTER-VISITES ---")

    # Tri des données 
    # On s'assure que les données sont ordonnées par patient puis par temps
    dataframe_clinical_data_copy = dataframe_clinical_data_copy.sort_values(by=['id', 'times'])

    # Calcul du temps écoulé depuis la visite précédente (unité en semaine)
    dataframe_clinical_data_copy['delta_weeks'] = dataframe_clinical_data_copy.groupby('id')['times'].diff()

    # Création du sous-ensemble pour le graphique (sans les NaN des premières visites)
    visites_suivi = dataframe_clinical_data_copy.dropna(subset=['delta_weeks'])

    # Visualisation de la distribution
    plt.figure(figsize=(10, 6))

    # Histogramme avec courbe de densité
    sns.histplot(visites_suivi['delta_weeks'], kde=True, bins=40, color='teal', alpha=0.6)

    # Ajout des repères visuels classiques pour le suivi médical
    plt.axvline(90, color='gray', linestyle=':', label='3 mois (90 jours)')
    plt.axvline(180, color='orange', linestyle='--', label='6 mois (180 jours)')
    plt.axvline(365, color='red', linestyle='--', label='1 an')

    plt.title('Distribution des délais entre les visites (Dataset pbc2)')
    plt.xlabel('Temps écoulé depuis la visite précédente (semaines)')
    plt.ylabel('Nombre de visites')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(DATA_DIR / "distribution_temps_inter_visites.png")
    plt.close()

    print("Distribution des temps de survie et évènement")


    # On trie par ID et temps, puis on prend la dernière ligne
    # C'est cette ligne qui contient le statut final et le temps total de suivi
    dataframe_clinical_data_copy_last = dataframe_clinical_data_copy.sort_values(by=['id', 'tte']).groupby('id').tail(1).copy()

    # Dictionnaire de mapping pour avoir les légendes des statuts.
    status_map = {
        0: 'Censuré (Vivant)',
        1: 'Transplanté',
        2: 'Décédé'
    }

    # On crée une colonne avec les noms explicites pour le graphique
    col_event = 'label'  
    dataframe_clinical_data_copy_last['event_label'] = dataframe_clinical_data_copy_last[col_event].map(status_map)

    # Distribution des statuts
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=dataframe_clinical_data_copy_last, x='event_label', palette='viridis',
                       order=['Censuré (Vivant)', 'Transplanté', 'Décédé'])

    plt.title('Répartition des patients par statut final')
    plt.xlabel('Statut')
    plt.ylabel('Nombre de patients')

    # Pour ajouter les nombres sur le graphiques
    for i in ax.containers:
        ax.bar_label(i, )
    plt.savefig(DATA_DIR / "distribution_statuts.png")
    plt.close()

    # Distribution des temps d'évènements.
    plt.figure(figsize=(10, 6))

    sns.histplot(
        data=dataframe_clinical_data_copy_last,
        x='tte',
        hue='event_label',
        hue_order=['Censuré (Vivant)', 'Transplanté', 'Décédé'],
        element="step",
        palette='viridis',
        alpha=0.3  # Transparence pour voir les superpositions
    )

    plt.title('Distribution des temps de suivi selon le type d\'évènement')
    plt.xlabel('Temps (semaines)')
    plt.ylabel('Nombre de patients')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(DATA_DIR / "distribution_temps_événement.png")
    plt.close()

if __name__ == "__main__":
    main()





