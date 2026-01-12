import pandas as pd

from clinical_cool_etud.config import DATA_DIR

def remove_total_protein(df):
    """
    Supprime la variable 'total_protein' du DataFrame.
    
    Parameters:
        df (pd.DataFrame): Le DataFrame contenant les données de cbp.
        
    Returns:
        pd.DataFrame: Le DataFrame après suppression de la colonne 'total_protein'.
    """
    return df.drop(columns=['total_protein'])

def correct_serBilir_for_patient_104(df):
    """
    Corrige l'erreur d'unité pour le patient 104 dans la variable 'serBilir'.
    
    Parameters:
        df (pd.DataFrame): Le DataFrame contenant les données de cbp.
        
    Returns:
        pd.DataFrame: Le DataFrame après correction des unités pour le patient 104.
    """
    df.loc[df['id'] == 104, 'serBilir'] = df.loc[df['id'] == 104, 'serBilir'] / 100
    return df

def remove_date_diag(df):
    """
    Supprime la variable 'date_diag' du DataFrame.
    
    Parameters:
        df (pd.DataFrame): Le DataFrame contenant les données de cbp.
        
    Returns:
        pd.DataFrame: Le DataFrame après suppression de la colonne 'date_diag'.
    """
    return df.drop(columns=['date_diag'])

def impute_continuous_variables(df):
    """
    Impute les valeurs manquantes dans les variables continues avec la médiane de la variable.
    
    Parameters:
        df (pd.DataFrame): Le DataFrame contenant les données de cbp.
        
    Returns:
        pd.DataFrame: Le DataFrame après imputation des valeurs manquantes pour les variables continues.
    """
    continuous_vars = ['serBilir', 'serChol', 'albumin', 'alkaline', 'SGOT', 'platelets', 'prothrombin']
    for col in continuous_vars:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=False)
            df.update(df[col].fillna(df[col].median()))
    return df

def impute_categorical_variables(df):
    """
    Impute les valeurs manquantes dans les variables catégorielles avec la mode de la variable.
    
    Parameters:
        df (pd.DataFrame): Le DataFrame contenant les données de cbp.
        
    Returns:
        pd.DataFrame: Le DataFrame après imputation des valeurs manquantes pour les variables catégorielles.
    """
    categorical_vars = ['ascites', 'hepatomegaly', 'spiders', 'edema', 'histologic']
    for col in categorical_vars:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode()[0], inplace=False)
            df.update(df[col].fillna(df[col].mode()[0]))
    return df

def replace_label_1_by_0_and_2_by_1(df):
    """
    Remplace les valeurs 1 par 0 et les valeurs 2 par 1 pour la colonne "label" du DataFrame passé en paramètre de la fonction.

    Parameters:
        df (pd.DataFrame): Le DataFrame contenant les données de cbp, avec une colonne 'label' à corriger.

    Returns:
        pd.DataFrame: Le DataFrame après remplacement des valeurs dans la colonne 'label'.
    """
    df.loc[df['label'] == 1, 'label'] = 0
    df.loc[df['label'] == 2, 'label'] = 1
    return df


def main():
    df = pd.read_csv(DATA_DIR / "clinical_data_pbc.csv")
    df = remove_total_protein(df)
    df = correct_serBilir_for_patient_104(df)
    df = remove_date_diag(df)
    df = impute_continuous_variables(df)
    df = impute_categorical_variables(df)
    df = replace_label_1_by_0_and_2_by_1(df)
    df.to_csv(DATA_DIR / "clinical_data_pbc_cleaned.csv", index=False)


