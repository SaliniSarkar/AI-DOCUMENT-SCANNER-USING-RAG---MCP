import pandas as pd


def load_csv(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    return dataframe.fillna("").to_string(index=False)
