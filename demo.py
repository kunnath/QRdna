import streamlit as st
import json
import os
import qrcode
import base64
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Directory to save files
SAVE_DIR = "saved_data"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_json_file(data, filename):
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)
    return filepath

def generate_qr_code(data, filename):
    qr = qrcode.make(data)
    qr_filepath = os.path.join(SAVE_DIR, filename)
    qr.save(qr_filepath)
    return qr_filepath

def decode_qr_code(qr_filepath):
    img = Image.open(qr_filepath)
    decoded_data = ""
    try:
        from pyzbar.pyzbar import decode
        qr_data = decode(img)
        if qr_data:
            decoded_data = qr_data[0].data.decode("utf-8")
    except ImportError:
        st.error("pyzbar module not found. Install with 'pip install pyzbar'.")
    return decoded_data

def compare_profiles_ai(profile1, profile2):
    # Combine text data from the profiles into strings for comparison
    profile1_text = " ".join(
        profile1.get("hobbies", []) +
        profile1.get("tastes", []) +
        profile1.get("skills", []) +
        profile1.get("preferences", [])
    )
    profile2_text = " ".join(
        profile2.get("hobbies", []) +
        profile2.get("tastes", []) +
        profile2.get("skills", []) +
        profile2.get("preferences", [])
    )

    # Vectorize the combined text data
    vectorizer = TfidfVectorizer().fit_transform([profile1_text, profile2_text])
    vectors = vectorizer.toarray()

    # Calculate the cosine similarity between the profiles
    similarity = cosine_similarity([vectors[0]], [vectors[1]])
    match_percentage = similarity[0][0] * 100  # Convert to percentage

    return match_percentage

def main():
    st.title("Profile JSON Generator and Comparison")

    # Tabs for separate sections
    tabs = ["Contact Sharing JSON Generator", "Compare Profiles", "Load JSON File to Generate QR Code", "Load and Decode QR Code"]
    choice = st.sidebar.selectbox("Select an option", tabs)

    if choice == "Contact Sharing JSON Generator":
        st.header("Contact Sharing JSON Generator")
        st.write("Enter your details below to generate and save a JSON file.")

        # Input fields for personal information
        name = st.text_input("Name", "")
        age = st.number_input("Age", min_value=0, max_value=150, value=0)
        email = st.text_input("Email", "")
        phone = st.text_input("Phone", "")
        address = st.text_area("Address", "")

        # Input fields for habits
        st.write("### Habits and Preferences")
        hobbies = st.text_area("Hobbies (comma-separated)", "")
        tastes = st.text_area("Tastes (comma-separated)", "")
        skills = st.text_area("Skills (comma-separated)", "")
        preferences = st.text_area("Preferences (comma-separated)", "")

        # Generate JSON data
        data = {
            "name": name,
            "age": age,
            "email": email,
            "phone": phone,
            "address": address,
            "hobbies": [item.strip() for item in hobbies.split(',') if item.strip()],
            "tastes": [item.strip() for item in tastes.split(',') if item.strip()],
            "skills": [item.strip() for item in skills.split(',') if item.strip()],
            "preferences": [item.strip() for item in preferences.split(',') if item.strip()],
        }

        # Save JSON file
        if st.button("Save JSON and Generate QR Code"):
            filename = f"{name.replace(' ', '_').lower()}_data.json"
            filepath = save_json_file(data, filename)
            qr_filepath = generate_qr_code(json.dumps(data, indent=4), f"{name.replace(' ', '_').lower()}_qr.png")
            st.success(f"Data saved as {filepath} and QR code generated at {qr_filepath}")

            st.download_button("Download JSON", data=json.dumps(data, indent=4), file_name=filename, mime="application/json")
            st.image(qr_filepath, caption="Generated QR Code")

    elif choice == "Compare Profiles":
        st.header("Compare Profiles")
        st.write("Select two profiles to compare their similarity.")

        # Profile selection input fields
        uploaded_file1 = st.file_uploader("Upload the first profile JSON file", type=["json"], key="file1")
        uploaded_file2 = st.file_uploader("Upload the second profile JSON file", type=["json"], key="file2")

        if uploaded_file1 and uploaded_file2:
            try:
                profile1 = json.load(uploaded_file1)
                profile2 = json.load(uploaded_file2)

                # Ensure all required keys are present in both profiles
                required_keys = ["hobbies", "tastes", "skills", "preferences"]
                for key in required_keys:
                    if key not in profile1:
                        profile1[key] = []  # Assign an empty list if key is missing
                    if key not in profile2:
                        profile2[key] = []  # Assign an empty list if key is missing

                # Compare profiles and display the similarity percentage
                match_percentage = compare_profiles_ai(profile1, profile2)
                st.success(f"AI-based Match Percentage: {match_percentage:.2f}%")

                if match_percentage > 70:
                    st.write("The profiles are highly similar!")
                elif match_percentage > 40:
                    st.write("The profiles have some similarities.")
                else:
                    st.write("The profiles have little in common.")

            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload valid JSON files.")
            except ValueError as e:
                st.error(f"Error during comparison: {e}")

    elif choice == "Load JSON File to Generate QR Code":
        st.header("Load JSON File to Generate QR Code")
        uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

        if uploaded_file:
            try:
                data = json.load(uploaded_file)
                filename = f"qr_{os.path.basename(uploaded_file.name).replace('.json', '.png')}"
                qr_filepath = generate_qr_code(json.dumps(data, indent=4), filename)
                st.success(f"QR code generated at {qr_filepath}")
                st.image(qr_filepath, caption="Generated QR Code")

            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON file.")

    elif choice == "Load and Decode QR Code":
        st.header("Load and Decode QR Code")
        uploaded_qr_file = st.file_uploader("Upload a QR code image file", type=["png", "jpg", "jpeg"])

        if uploaded_qr_file:
            image = Image.open(uploaded_qr_file)
            decoded_data = decode_qr_code(image)
            if decoded_data:
                st.success("QR code successfully decoded!")
                st.text_area("Decoded JSON data", decoded_data, height=300)
            else:
                st.error("Failed to decode QR code. Please ensure the file is a valid QR code image.")

if __name__ == "__main__":
    main()