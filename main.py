import pandas as pd

def get_clean_work_time(work_time_path):
  return (pd.read_csv(work_time_path, sep=';', encoding='utf-8')
        .drop_duplicates()
        .fillna({'Temps annuel de travail (SNCF)': 0, 
                  'Temps annuel de travail (France)': 0, 
                  'Commentaires': ''})
        .astype({'Date': int, 
                  'Temps annuel de travail (SNCF)': int, 
                  'Temps annuel de travail (France)': int})
        .assign(Commentaires=lambda x: x['Commentaires'].str.strip()))

def get_interesting_columns(df, columns):
  missing_columns = [col for col in columns if col not in df.columns]
  if missing_columns:
    print(f"Columns missing")
    return pd.DataFrame()
  return df[columns]


frequentation = pd.read_csv("./data/frequentation-gares.csv")

print(work_time)
print(frequentation)
