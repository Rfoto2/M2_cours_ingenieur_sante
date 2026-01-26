from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import torch

from clinical_cool_etud.NLLsurv import NLLSurvLoss
from clinical_cool_etud.config import DATA_DIR
from clinical_cool_etud.model import LSTM_risk_estimator
from clinical_cool_etud.prepa_data_model import build_lstm_tensor, split_tensors_stratified
from clinical_cool_etud.sksurv_format import to_sksurv_format


def main():

    # Charger les données

    data_pbc = pd.read_csv(DATA_DIR / "clinical_data_pbc_cleaned.csv")

    list_features_continuous = ["age", "edema", "serBilir", "serChol", "albumin", "alkaline", "SGOT", "platelets", "prothrombin", "histologic"]
    list_features_binary = ["drug", "sex", "ascites", "hepatomegaly", "spiders"]

    time_to_event_column = "tte"
    event_column = "label"

    number_features = len(list_features_continuous) + len(list_features_binary)

    # Construction des tenseurs
    X_tensor, y_tensor, all_ids = build_lstm_tensor(
        data_pbc,  # Ton dataframe longitudinal complet (pas le baseline !)
        id_col='id',
        tte_col=time_to_event_column,
        event_col=event_column,
        feature_continuous_cols=list_features_continuous,
        features_binary_cols=list_features_binary,
    )

    # Split et datasets

    X_train, X_test, Y_train, Y_test = split_tensors_stratified(X_tensor, y_tensor)

    # Tensordataset : necessaire pour utiliser le dataloader (création des batchs)
