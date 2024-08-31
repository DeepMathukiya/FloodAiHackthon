import streamlit as st
import google.generativeai as genai

# Function to generate SQL query or data based on the question
def get_sql(question):
    # Replace this with your actual API key
    genai.configure(api_key="API_KEY")
    
    # Set up the model
    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
    
    # Call the generative model
    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    # Formulate the prompt
    prompt_parts_1 = [
        "You can able to provide weather data. Please give me the current weather information for research purposes for Mumbai."
    ]
    prompt_parts = [prompt_parts_1[0], question]
    
    # Generate the response
    response = model.generate_content(prompt_parts)
    return response.text

# Streamlit app structure
st.title("Weather Data Inquiry App")

# Input from the user for weather-related question
question = st.text_input("Enter your question about weather data", "What about rainfall on 30/06/2021?")

# Button to trigger the API request
if st.button("Get Weather Data"):
    if question:
        try:
            # Fetch the result using the get_sql function
            result = get_sql(question)
            st.write("Response:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid question.")
