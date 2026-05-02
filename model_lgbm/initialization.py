import pickle
import pandas as pd
from model_lgbm.data_preprocessing import preprocess_patient
import shap
import os

threshold = 0.21

model_path = os.path.join(os.path.dirname(__file__), 'lgbm_sepsis_model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

explainer = shap.TreeExplainer(model)

def predict(df_raw):
    X = preprocess_patient(df_raw)
    probs = model.predict(X)
    preds = (probs >= threshold).astype(int)
    return probs, preds