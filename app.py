import streamlit as st
import qrcode
from io import BytesIO
import base64
import json
import os

# Directory to save files
SAVE_DIR = "saved_data"
os.makedirs(SAVE_DIR, exist_ok=True)

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

# Function to save JSON file
def save_json_file(data, filename):
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)
    return filepath

# Function to load JSON from file
def load_json_file(filepath):
    with open(filepath, "r") as json_file:
        return json.load(json_file)

# Streamlit app
def main():
    st.title("Contact Sharing QR Code Generator")
    st.write("Enter your details below to generate and save a QR code and JSON file.")

    # Input fields for personal information
    name = st.text_input("Name", "")
    age = st.number_input("Age", min_value=0, max_value=150, value=0)
    email = st.text_input("Email", "")
    phone = st.text_input("Phone", "")
    address = st.text_area("Address", "")

    # Input fields for habits
    st.write("### Habits and Preferences")
    morning_routine = st.text_area("Morning Routine (comma-separated)", "")
    dietary_preferences = st.text_area("Dietary Preferences (comma-separated)", "")
    hobbies = st.text_area("Hobbies (comma-separated)", "")
    bedtime = st.text_input("Bedtime", "")
    wake_time = st.text_input("Wake Time", "")

    # Generate JSON data
    data = {
        "name": name,
        "age": age,
        "email": email,
        "phone": phone,
        "address": address,
        "habits": {
            "morning_routine": [item.strip() for item in morning_routine.split(',') if item.strip()],
            "dietary_preferences": [item.strip() for item in dietary_preferences.split(',') if item.strip()],
            "hobbies": [item.strip() for item in hobbies.split(',') if item.strip()],
            "sleep_schedule": {
                "bedtime": bedtime,
                "wake_time": wake_time,
            },
        },
    }

    # Save JSON file and generate QR code
    if st.button("Save JSON and Generate QR Code"):
        filename = f"{name.replace(' ', '_').lower()}_data.json"
        filepath = save_json_file(data, filename)
        st.success(f"Data saved as {filepath}")

        json_data = json.dumps(data, indent=4)
        qr_image_bytes = generate_qr_code(json_data)
        st.image(qr_image_bytes, caption="Your QR Code", use_column_width=True)

        # Download link for QR code
        qr_download_link = f'<a href="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode()}" download="qr_code.png">Download QR Code</a>'
        st.markdown(qr_download_link, unsafe_allow_html=True)

    # Load JSON file to generate QR code
    st.write("### Load JSON File to Generate QR Code")
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    if uploaded_file:
        loaded_data = json.load(uploaded_file)
        qr_image_bytes = generate_qr_code(json.dumps(loaded_data, indent=4))
        st.image(qr_image_bytes, caption="QR Code from Uploaded JSON", use_column_width=True)

        # Download link for QR code
        qr_download_link = f'<a href="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode()}" download="uploaded_qr_code.png">Download QR Code</a>'
        st.markdown(qr_download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()