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

work_time_file = get_clean_work_time('data/temps-de-travail-annuel-depuis-1851.csv')
work_time_columns = [
  "Date",
  "Temps annuel de travail (SNCF)",
  "Temps annuel de travail (France)"  
  ]
work_time_filtered_columns = get_interesting_columns(work_time_file, work_time_columns)
work_time_filtered_rows = work_time_filtered_columns[
  (work_time_filtered_columns['Date'].astype(str) == '2017') | (work_time_filtered_columns['Date'].astype(str) == '2018')
  ]
work_time = work_time_filtered_rows

frequentation_file = pd.read_csv("./data/frequentation-gares.csv", sep=";")
frequentation_columns = [
  "Nom de la gare",
  "Code postal",
  "Total Voyageurs + Non voyageurs 2017",
  "Total Voyageurs + Non voyageurs 2018"
  ]
frequentation_filtered_columns = get_interesting_columns(frequentation_file, frequentation_columns)
frequentation_filtered_rows = frequentation_filtered_columns[
  frequentation_filtered_columns[
    'Code postal'
  ].astype(str).str[:1] == '7'].head(3)
frequentation = frequentation_filtered_rows


print(work_time)
print("\n\n\n")
print(frequentation)
