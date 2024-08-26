import pandas as pd


def load_rainfall_data(file_path):
    # Load the data from an XLSX file
    try:
        df = pd.read_excel(file_path, engine='openpyxl')  # Specify engine if needed
    except Exception as e:
        raise ValueError(f"Error loading XLSX file: {e}")
    return df

def get_predicted_rainfall(date, year, df):
    # Check if year is 2021
    if year != 2021:
        return "can't predict"
    
    # Check if the date is in the data
    filtered_df = df[df['date'] == date]
    if not filtered_df.empty:
        return filtered_df['rainfall'].values[0]
    else:
        return "Date not found in the data"

    # File path in Google Drive
file_path = 'meow.xlsx'  # Change this to the path of your file in Drive
df = load_rainfall_data(file_path)
    
date = input("Enter the date (in MM-DD format): ")
year = int(input("Enter the year: "))
    
predicted_rainfall = get_predicted_rainfall(date, year, df)
print(f"Predicted rainfall: {predicted_rainfall}")

