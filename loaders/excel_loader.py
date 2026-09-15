import pandas as pd


def load_excel(uploaded_file):
    excel_data = pd.read_excel(uploaded_file, sheet_name=None)
    parts = []

    for sheet_name, dataframe in excel_data.items():
        parts.append(f"Sheet: {sheet_name}")
        if dataframe.empty:
            parts.append("(empty sheet)")
        else:
            parts.append(dataframe.fillna("").to_string(index=False))

    return "\n\n".join(parts)
