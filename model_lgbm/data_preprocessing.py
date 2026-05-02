selected_features = [
    'ICULOS',
    'FiO2_Freq_6h',
    'Unit1',
    'Temp_Max_6h',
    'Alkalinephos',
    'Creatinine',
    'HospAdmTime',
    'HCO3',
    'WBC',
    'ShockIndex',
    'Temp',
    'PaCO2_Freq_12h',
    'Platelets',
    'Resp_Mean_12h',
    'BUN',
    'EtCO2_missing',
    'Temp_Max_2h',
    'HR_Max_6h',
    'Temp_Max_12h',
    'Calcium',
    'SBP_Min_6h',
    'Chloride_Mean_12h',
    'Age',
    'SBP_Std_6h',
    'Lactate_Mean_12h',
    'PTT',
    'Lactate_Freq_6h',
    'Glucose',
    'Bilirubin_total_Mean_6h',
    'BUN/CR',
    'FiO2',
    'Fibrinogen',
    'AST',
    'Resp_Min_12h',
    'PTT_Mean_12h',
    'Bilirubin_total_Mean_12h',
    'Magnesium',
    'DBP_Min_12h',
    'Temp_Min_12h',
    'Resp_Mean_6h',
    'FiO2_Mean_12h',
    'MAP_Min_12h',
    'HR_Min_12h',
    'Hct',
    'BaseExcess_Mean_12h',
    'DBP_Max_12h',
    'TroponinI',
    'MAP_Min_2h',
    'Resp_Max_12h',
    'Hgb',
    'PaCO2_Mean_12h',
    'AST_Mean_12h',
    'Bilirubin_direct',
    'pH_Mean_12h',
    'SBP_Min_12h',
    'MAP_Min_6h',
    'O2Sat_Mean_12h',
    'Chloride',
    'HR_Max_12h',
    'PTT_Mean_6h',
    'SaO2_Mean_12h',
    'DBP_Mean_12h',
    'Potassium',
    'Phosphate_Mean_12h',
    'MAP_Max_12h',
    'O2Sat_Std_6h',
    'Temp_Mean_12h',
    'SBP_Max_12h',
    'DBP_Min_6h',
    'Alkalinephos_Mean_12h',
    'O2Sat_Min_6h',
    'Lactate',
    'PaCO2',
    'O2Sat_Min_12h',
    'Alkalinephos_Freq_6h',
    'SaO2_Mean_6h',
    'SBP_Min_2h',
    'Phosphate',
    'HR_Max_2h',
    'SBP_Mean_12h',
    'BaseExcess_Mean_6h',
    'SaO2_Freq_12h',
    'EtCO2_Freq_6h',
    'Resp_Std_2h',
    'MAP_Mean_12h',
    'SBP_Std_12h',
    'EtCO2_Mean_12h',
    'EtCO2_Mean_6h',
    'HR_Std_12h',
    'Resp_Max_2h',
    'SBP_Max_6h',
    'O2Sat_Std_12h',
    'HR_Mean_12h',
    'DBP_Max_6h',
    'SBP_Std_2h',
    'pH_Mean_6h',
    'Chloride_Freq_12h',
    'Resp_Max_6h',
    'MAP_Max_6h',
    'PTT_Freq_12h',
    'EtCO2',
    'Alkalinephos_Mean_6h',
    'O2Sat_Max_12h',
    'HR',
    'Lactate_Freq_12h',
    'Temp_Min_6h',
    'PaCO2_Freq_6h',
    'DBP_Min_2h',
    'Resp_Std_12h',
    'MAP_Std_6h',
    'SBP_Max_2h',
    'Temp_Std_12h',
    'SaO2_Freq_6h',
    'pH',
    'DBP_Mean_6h',
    'SaO2',
    'Chloride_Mean_6h',
    'FiO2_Mean_6h',
    'Alkalinephos_Freq_12h',
    'DBP_Std_12h',
    'Gender',
    'Phosphate_Mean_6h'
 ]

def preprocess_patient(df_raw):
    df = df_raw.copy()
    df = df.sort_values('ICULOS').reset_index(drop=True)
    
    exclude_cols = ['ICULOS', 'SepsisLabel', 'Age', 'Gender', 'Unit1', 'Unit2', 'HospAdmTime']
    clinical_cols = [col for col in df.columns if col not in exclude_cols]
    for col in clinical_cols:
        df[f'{col}_missing'] = df[col].isna().astype(int)
    
    lab_names = ["Lactate", "FiO2", "PaCO2", "pH", "BaseExcess", "Alkalinephos", 
                 "AST", "Bilirubin_total", "SaO2", "PTT", "Chloride", "Phosphate", "EtCO2"]
    for name in lab_names:
        df[f'{name}_Freq_6h'] = df[name].isna().map({True:0, False:1}).rolling(6, min_periods=1).sum()
        df[f'{name}_Freq_12h'] = df[name].isna().map({True:0, False:1}).rolling(12, min_periods=1).sum()
        filled = df[name].ffill()
        df[f'{name}_Mean_6h'] = filled.rolling(6, min_periods=1).mean()
        df[f'{name}_Mean_12h'] = filled.rolling(12, min_periods=1).mean()
    
    df = df.ffill()
    
    df['ShockIndex'] = df['HR'] / df['SBP']
    df['BUN/CR'] = df['BUN'] / df['Creatinine']
    
    vital_features = ["HR", "O2Sat", "Temp", "SBP", "MAP", "DBP", "Resp"]
    for name in vital_features:
        for w in [2, 3, 6, 12]:
            df[f'{name}_Min_{w}h'] = df[name].rolling(w, min_periods=1).min()
            df[f'{name}_Max_{w}h'] = df[name].rolling(w, min_periods=1).max()
            df[f'{name}_Mean_{w}h'] = df[name].rolling(w, min_periods=1).mean()
            df[f'{name}_Std_{w}h'] = df[name].rolling(w, min_periods=1).std()
    
    return df[selected_features]