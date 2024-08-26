import streamlit as st
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the model once during app startup
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('segmentation.h5')
    # Compile the model (optional) to avoid the warning
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model = load_model()

# Function to predict the class and segmentation mask
def predict_image(image, model):
    # Resize and normalize image
    image = image.resize((128, 128))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    
    # Model predictions
    class_pred, mask_pred = model.predict(image)
    
    # Squeeze the mask output to remove batch dimension (e.g., shape (1, 128, 128, 1) -> (128, 128))
    mask_pred = np.squeeze(mask_pred)
    
    return class_pred, mask_pred

# Function to plot the original image, predicted mask, and overlayed image
def plot_predictions(image, mask_pred):
    # Create a figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # Subplot 1: Original Image
    axes[0].imshow(image)
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    # Subplot 2: Predicted Mask
    axes[1].imshow(mask_pred, cmap='gray')
    axes[1].set_title('Predicted Mask')
    axes[1].axis('off')

    # Subplot 3: Overlayed Image and Mask
    axes[2].imshow(image)
    axes[2].imshow(mask_pred, cmap='jet', alpha=0.5)
    axes[2].set_title('Overlayed Image')
    axes[2].axis('off')

    st.pyplot(fig)

# Streamlit app title and description
st.title("Flood Detection and Segmentation")
st.write("Upload an image to get the flood classification and segmentation mask.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the uploaded image
    image = Image.open(uploaded_file)
    
    # Display uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")

    # Predict the class and segmentation mask
    class_pred, mask_pred = predict_image(image, model)

    # Display the classification result
    st.write(f"Flooded: {'Yes' if class_pred > 0.5 else 'No'} (Confidence: {class_pred[0][0]:.2f})")

    # Plot the original image, mask, and overlay
    plot_predictions(image, mask_pred)
