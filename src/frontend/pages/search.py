import streamlit as st
import cv2
import numpy as np

st.sidebar.header("Search")


# Set up the Streamlit app
st.title("Image Upload and Text Search App")

# Input section for search term
search_term = st.text_input("Enter a search term:")

# Image upload functionality
uploaded_file = st.file_uploader("Upload an image...", type=['jpg', 'jpeg', 'png'])

# Display the uploaded image if available
if uploaded_file is not None:
    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    uploaded_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Display the uploaded image
    st.image(uploaded_image, channels="BGR", caption='Uploaded Image', use_column_width=True)

# Display results based on search term or uploaded image
if search_term:
    st.write(f"Results for: **{search_term}**")

# Allow for text display based on the uploaded image (for demonstration)
if uploaded_file is not None:
    st.write("You uploaded an image, and you can provide a search term for further queries.")
