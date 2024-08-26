import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Load the model
model = load('random_forest_model.joblib')

# Load and preprocess the data
df = pd.read_csv('combined_rainfall_data.csv')
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek
df['rainfall_lag1'] = df.groupby(['lat', 'lon'])['rainfall'].shift(1)
df = df.dropna()

# Define features
features = ['lat', 'lon', 'year', 'month', 'day', 'dayofweek', 'rainfall_lag1']

# Streamlit app layout
st.title('Rainfall Prediction App')

st.sidebar.header('Input Parameters')

# Date input
date = st.sidebar.date_input('Date', pd.to_datetime('today'))

# Latitude and Longitude input
lat = st.sidebar.number_input('Latitude', value=19.0)
lon = st.sidebar.number_input('Longitude', value=72.0)

if st.sidebar.button('Predict'):
    # Create DataFrame for input data
    input_data = pd.DataFrame({
        'date': [pd.to_datetime(date)],
        'lat': [lat],
        'lon': [lon]
    })

    # Add time-based features
    input_data['year'] = input_data['date'].dt.year
    input_data['month'] = input_data['date'].dt.month
    input_data['day'] = input_data['date'].dt.day
    input_data['dayofweek'] = input_data['date'].dt.dayofweek

    # Add lag feature
    try:
        input_data['rainfall_lag1'] = df[(df['lat'] == lat) & (df['lon'] == lon)]['rainfall'].iloc[-1]
    except IndexError:
        input_data['rainfall_lag1'] = np.nan

    # Make prediction
    try:
        prediction = model.predict(input_data[features])
        st.write(f'Predicted Rainfall: {prediction[0]:.2f}')
    except Exception as e:
        st.write(f'Error: {e}')

