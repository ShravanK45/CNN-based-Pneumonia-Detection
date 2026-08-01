import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Pneumonia Detection",
    page_icon="🫁",
    layout="centered"
)

st.title("🫁 Pneumonia Detection using CNN")

st.write(
    "Upload a Chest X-Ray image to predict whether it is NORMAL or PNEUMONIA."
)

# -------------------------
# Load Model
# -------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(r"notebooks\best_pneumonia_model.keras")

model = load_model()

# -------------------------
# Image Preprocessing
# -------------------------

IMG_SIZE = 150

def preprocess_image(image):

    image = image.convert("L")          # Convert to grayscale
    image = image.resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image)
    image = image.astype("float32") / 255.0
    image = image.reshape(1, IMG_SIZE, IMG_SIZE, 1)
    return image

# -------------------------
# Upload Image
# -------------------------

uploaded_file = st.file_uploader(
    "Upload Chest X-Ray",
    type=["jpg","jpeg","png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded X-Ray", use_container_width=True)
    processed = preprocess_image(image)
    prediction = model.predict(processed)
    probability = prediction[0][0]

    if probability >= 0.5:

        label = "NORMAL"
        confidence = probability
        st.success(f"Prediction : {label}")

    else:

        label = "PNEUMONIA"
        confidence = 1 - probability
        st.error(f"Prediction : {label}")

    st.metric(
        "Confidence",
        f"{confidence*100:.2f}%"
    )
