import streamlit as st
import pandas as pd

def load_rainfall_data(file_path):
    # Load the data from an XLSX file
    try:
        df = pd.read_excel(file_path, engine='openpyxl')  # Specify engine if needed
    except Exception as e:
        st.error(f"Error loading XLSX file: {e}")
        return None
    return df

def get_predicted_rainfall(date, df):
    # Check if the date is in the data
    filtered_df = df[df['date'] == date]
    if not filtered_df.empty:
        return filtered_df['rainfall'].values[0]
    else:
        return "Date not found in the data"

def main():
    st.title("Rainfall Prediction")

    # File upload
    
    df = load_rainfall_data("meow.xlsx")
    if df is not None:
             # Input field
            date = st.text_input("Enter the date (in MM-DD format):")
            
            if st.button("Predict"):
                if date:
                    predicted_rainfall = get_predicted_rainfall(date, df)
                    st.write(f"Predicted rainfall: {predicted_rainfall}")
                else:
                    st.error("Please provide a date")

if __name__ == "__main__":
    main()
