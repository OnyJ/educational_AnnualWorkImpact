import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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
  # "Temps annuel de travail (France)"  
  ]
work_time_filtered_columns = get_interesting_columns(work_time_file, work_time_columns)
work_time_filtered_rows = work_time_filtered_columns[
  (work_time_filtered_columns['Date'].astype(str).astype(int).between(2014, 2018))
]
work_time = work_time_filtered_rows

frequentation_file = pd.read_csv("./data/frequentation-gares.csv", sep=";")
frequentation_columns = [
  "Nom de la gare",
  "Code postal",
  "Total Voyageurs + Non voyageurs 2020",
  "Total Voyageurs + Non voyageurs 2021",
  "Total Voyageurs + Non voyageurs 2022",
  "Total Voyageurs + Non voyageurs 2023"
  ]
frequentation_filtered_columns = get_interesting_columns(frequentation_file, frequentation_columns)
frequentation_filtered_rows = frequentation_filtered_columns[
  frequentation_filtered_columns[
    'Code postal'
  ].astype(str).str[:2] == '75'].head(8)
frequentation = frequentation_filtered_rows

# ****************************************

def get_frequentation_diagram(frequentation):
  frequentation_df = pd.DataFrame(frequentation)
  frequentation_df.set_index('Nom de la gare') [
    ["Total Voyageurs + Non voyageurs 2020",
     "Total Voyageurs + Non voyageurs 2021",
     "Total Voyageurs + Non voyageurs 2022",
     "Total Voyageurs + Non voyageurs 2023"]].plot(kind='bar', figsize=(12, 6))
  plt.title('Comparaison fréquentation des gares entre 2017 et 2018')
  plt.ylabel('Total voyageurs')
  plt.xlabel('Nom de la gare')
  plt.xticks(rotation=45)
  plt.grid(axis='y')
  plt.legend(title="Année")
  plt.show()

# ****************************************
# Display

# print("WORK TIME")
# print(work_time)
# print("\n\n\n")

print("FREQUENTATION")
print(frequentation)
print("\n\n\n")

# print("FREQUENTATION PRETTY DATA")

# get_frequentation_diagram(frequentation)



# ****************************************
# Deep Learning


# TODO : Add column for annual growth between 2022 and 2023

# df = pd.DataFrame(frequentation)
# df["Croissance annuelle"] = (
#   (df["Total Voyageurs + Non voyageurs 2023"] - df["Total Voyageurs + Non voyageurs 2022"]) / df["Total Voyageurs + Non voyageurs 2022"])
# df.head()
# 
# df["Total Voyageurs + Non voyageurs 2024 (estimé)"] = (
#   df["Total Voyageurs + Non voyageurs 2023"] * (1 + df["Croissance annuelle"])
# )
# 
# # Variable explicative X
# x = df[["Total Voyageurs + Non voyageurs 2023", "Croissance annuelle"]]
# # Variable Cible Y
# y = df["Total Voyageurs + Non voyageurs 2024 (estimé)"]
# 
# model = LinearRegression()
# model.fit(x, y)
# 
# print("Coefficients : ", model.coef_)
# print("Intercept : ", model.intercept_)
# 
# df["Prédiction 2024"] = model.predict(x)
# print(df[["Nom de la gare", "Prédiction 2024"]])


def predict_frequentation(df, prediction_year, history_start_year, history_end_year):
    """
    Predicts attendance for a future year, using historical data.
    Returns : a DataFrame with predictions added in a new column
    """

    historical_years_columns = [f"Total Voyageurs + Non voyageurs {year}" for year in range(history_start_year, history_end_year + 1)]
    
    # Check that historical columns exist
    if not all(col in df.columns for col in historical_years_columns):
        raise ValueError("Certaines colonnes historiques sont manquantes dans le DataFrame.")
    
    # Calculation of average annual growth for each station
    for year in range(history_start_year, history_end_year):
        col_current = f"Total Voyageurs + Non voyageurs {year}"
        col_next = f"Total Voyageurs + Non voyageurs {year + 1}"
        df[f"Croissance {year}-{year+1}"] = (df[col_next] - df[col_current]) / df[col_current]
    
    average_growth_cols = [f"Croissance {year}-{year+1}" for year in range(history_start_year, history_end_year)]
    df["Croissance moyenne"] = df[average_growth_cols].mean(axis=1)
    
    # Prediction for target year
    last_column = f"Total Voyageurs + Non voyageurs {history_end_year}"
    df[f"Prédiction {prediction_year}"] = df[last_column] * (1 + df["Croissance moyenne"])
    
    # Clean up temporary columns
    df.drop(columns=average_growth_cols + ["Croissance moyenne"], inplace=True)
    
    return df


# ****************************************
# Charger le CSV contenant les données (à adapter selon le chemin et le nom)

# df_frequentation = pd.read_csv("data/frequentation-gares.csv")

df_attendance_in_2024 = predict_frequentation(frequentation, prediction_year=2024, history_start_year=2020, history_end_year=2023)

print(df_attendance_in_2024[["Nom de la gare", "Total Voyageurs + Non voyageurs 2023", "Prédiction 2024"]])

average_growth_cols = [f"Croissance {year}-{year+1}" for year in range(2020, 2023)]
df_attendance_in_2024["Croissance moyenne"] = frequentation[average_growth_cols].mean(axis=1)

print(df_attendance_in_2024[["Nom de la gare", "Total Voyageurs + Non voyageurs 2023", "Croissance moyenne", "Prédiction 2024"]])
