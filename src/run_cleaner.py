import re
import pandas as pd

df = pd.read_csv("./data/raw/rents/mokotow_rents.csv")

def clean_area(value: str):
    if pd.isna(value):
        return None
    
    match = re.search(r'(\d+(?:\.\d+)?)', str(value))
    if match:
        return float(match.group(1))
    return None

    
print(df.head(100))