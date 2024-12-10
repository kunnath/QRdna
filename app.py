import streamlit as st
import json
import os
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import numpy as np
from difflib import SequenceMatcher

# Directory to save files
SAVE_DIR = "saved_data"
os.makedirs(SAVE_DIR, exist_ok=True)

# Helper Functions
def save_json_file(data, filename):
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)
    return filepath

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    qr_filepath = os.path.join(SAVE_DIR, filename)
    img.save(qr_filepath)
    return qr_filepath

def decode_qr_code(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        qr_data = decode(image)
        if qr_data:
            return qr_data[0].data.decode("utf-8")
        else:
            return "No QR code found in the uploaded image."
    except Exception as e:
        return f"Error decoding QR code: {e}"

def calculate_similarity(profile1, profile2):
    """
    Compares two JSON profiles and calculates similarity percentage.
    """
    profile1_text = json.dumps(profile1, sort_keys=True)
    profile2_text = json.dumps(profile2, sort_keys=True)
    similarity = SequenceMatcher(None, profile1_text, profile2_text).ratio()
    return similarity * 100

def scan_qr_code_from_camera():
    """
    Scans QR codes using the device's camera and extracts data.
    """
    st.write("**Starting camera... Press 'Stop Scanning' to quit.**")
    cap = cv2.VideoCapture(1)
    qr_data = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera.")
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            points = obj.polygon
            if len(points) == 4:
                pts = np.array([(p.x, p.y) for p in points], dtype=np.int32)
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

            # Display detected QR data
            cv2.putText(frame, f"Data: {qr_data}", (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       # st.image(frame_rgb, caption="Scanning...", use_container_width=True)

        if qr_data:
            break

    cap.release()
    return qr_data

def live_compare(default_profile):
    """
    Live compare default profile with QR Code scanned using camera.
    """
    st.header("Live Compare QR Code with Default Profile")
    st.json(default_profile)

    if st.button("Start Scanning"):
        scanned_data = scan_qr_code_from_camera()
        if scanned_data:
            try:
                scanned_profile = json.loads(scanned_data)
                st.success("Scanned Profile:")
                st.json(scanned_profile)

                similarity = calculate_similarity(default_profile, scanned_profile)
                st.write(f"**Match Percentage:** {similarity:.2f}%")

                if similarity == 100.0:
                    st.success("Exact Match!")
                elif similarity > 80.0:
                    st.info("Profiles are highly similar.")
                else:
                    st.warning("Profiles are significantly different.")
            except json.JSONDecodeError:
                st.error("Scanned QR code does not contain valid profile data.")

def compare_profiles():
    """
    Compares two uploaded JSON profiles.
    """
    st.header("Compare Uploaded Profiles")
    file1 = st.file_uploader("Upload Profile 1", type="json")
    file2 = st.file_uploader("Upload Profile 2", type="json")

    if file1 and file2:
        try:
            profile1 = json.load(file1)
            profile2 = json.load(file2)

            similarity = calculate_similarity(profile1, profile2)
            st.write(f"**Profile Similarity:** {similarity:.2f}%")

            if similarity == 100.0:
                st.success("Profiles are an exact match!")
            elif similarity > 80.0:
                st.info("Profiles are highly similar.")
            else:
                st.warning("Profiles are significantly different.")
        except Exception as e:
            st.error(f"Error comparing profiles: {e}")

# Streamlit App
def main():
    st.title("QR Code Profile Management")

    # Default profile for live comparison
    default_profile = {
        "name": "Sreelesh",
        "age": 30,
        "email": "aikunnath@example.com",
        "phone": "+1234567890",
        "address": "Prendener Str.12, Berlin, Germany",
        "hobbies": ["reading", "traveling"],
        "tastes": ["spicy", "savory"],
        "skills": ["programming", "data analysis"],
        "preferences": ["outdoor activities", "coffee"],
    }

    options = ["Generate Profile and QR Code", "Compare Profiles", "Live Compare Default Profile"]
    choice = st.sidebar.selectbox("Choose an option", options)

    if choice == "Generate Profile and QR Code":
        st.header("Generate Profile and QR Code")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=150, step=1)
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        hobbies = st.text_area("Hobbies (comma-separated)").split(",")
        tastes = st.text_area("Tastes (comma-separated)").split(",")
        skills = st.text_area("Skills (comma-separated)").split(",")
        preferences = st.text_area("Preferences (comma-separated)").split(",")

        profile = {
            "name": name,
            "age": age,
            "email": email,
            "phone": phone,
            "address": address,
            "hobbies": [h.strip() for h in hobbies if h.strip()],
            "tastes": [t.strip() for t in tastes if t.strip()],
            "skills": [s.strip() for s in skills if s.strip()],
            "preferences": [p.strip() for p in preferences if p.strip()],
        }

        if st.button("Generate"):
            filename = f"{name.lower().replace(' ', '_')}.json"
            save_json_file(profile, filename)
            qr_filename = f"{name.lower().replace(' ', '_')}_qr.png"
            qr_filepath = generate_qr_code(json.dumps(profile), qr_filename)
            st.image(qr_filepath, caption="Generated QR Code")
            st.download_button("Download JSON", json.dumps(profile, indent=4), filename)

    elif choice == "Compare Profiles":
        compare_profiles()

    elif choice == "Live Compare Default Profile":
        live_compare(default_profile)

if __name__ == "__main__":
    main()