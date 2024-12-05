# app.py
import streamlit as st
import qrcode
from io import BytesIO
import base64
import json
import os
from PIL import Image
import pyzbar.pyzbar as pyzbar

# Directory to save files
SAVE_DIR = "saved_data"
os.makedirs(SAVE_DIR, exist_ok=True)

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

def save_json_file(data, filename):
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)
    return filepath

def load_json_file(filepath):
    with open(filepath, "r") as json_file:
        return json.load(json_file)

def decode_qr_code(file):
    img = Image.open(file)
    decoded_objects = pyzbar.decode(img)
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    return None

def main():
    st.title("QR Code Generator and Decoder")

    # Tabs for separate sections
    tabs = ["Contact Sharing QR Code Generator", "Load JSON File to Generate QR Code", "Load and Decode QR Code"]
    choice = st.sidebar.selectbox("Select an option", tabs)

    if choice == "Contact Sharing QR Code Generator":
        st.header("Contact Sharing QR Code Generator")
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

    elif choice == "Load JSON File to Generate QR Code":
        st.header("Load JSON File to Generate QR Code")
        uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
        if uploaded_file:
            try:
                loaded_data = json.load(uploaded_file)
                qr_image_bytes = generate_qr_code(json.dumps(loaded_data, indent=4))
                st.image(qr_image_bytes, caption="QR Code from Uploaded JSON", use_column_width=True)

                # Download link for QR code
                qr_download_link = f'<a href="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode()}" download="uploaded_qr_code.png">Download QR Code</a>'
                st.markdown(qr_download_link, unsafe_allow_html=True)
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON.")

    elif choice == "Load and Decode QR Code":
        st.header("Load and Decode QR Code")
        uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            decoded_data = decode_qr_code(uploaded_file)
            if decoded_data:
                st.success("QR Code Decoded Successfully!")
                st.json(json.loads(decoded_data))

                # Save decoded data to JSON file
                decoded_json = json.loads(decoded_data)
                save_path = save_json_file(decoded_json, "decoded_data.json")
                st.write(f"Decoded data saved as {save_path}")

                # Map data back to fields
                st.write("### Mapped Data")
                st.text_input("Name", decoded_json.get("name", ""))
                st.number_input("Age", min_value=0, max_value=150, value=decoded_json.get("age", 0))
                st.text_input("Email", decoded_json.get("email", ""))
                st.text_input("Phone", decoded_json.get("phone", ""))
                st.text_area("Address", decoded_json.get("address", ""))

                habits = decoded_json.get("habits", {})
                st.text_area("Morning Routine", ", ".join(habits.get("morning_routine", [])))
                st.text_area("Dietary Preferences", ", ".join(habits.get("dietary_preferences", [])))
                st.text_area("Hobbies", ", ".join(habits.get("hobbies", [])))
                sleep_schedule = habits.get("sleep_schedule", {})
                st.text_input("Bedtime", sleep_schedule.get("bedtime", ""))
                st.text_input("Wake Time", sleep_schedule.get("wake_time", ""))
            else:
                st.error("Unable to decode QR Code. Please upload a valid QR Code image.")

if __name__ == "__main__":
    main()
