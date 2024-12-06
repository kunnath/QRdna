import streamlit as st
import json
import os
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

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
        # Open the uploaded file as an image
        image = Image.open(uploaded_file)
        # Decode the QR code
        qr_data = decode(image)
        if qr_data:
            return qr_data[0].data.decode("utf-8")
        else:
            return "No QR code found in the uploaded image."
    except Exception as e:
        return f"Error decoding QR code: {e}"

def compare_profiles_ai(profile1, profile2):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Combine profile attributes into strings for comparison
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

    # Vectorize and calculate similarity
    vectorizer = CountVectorizer().fit_transform([profile1_text, profile2_text])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1] * 100  # Return percentage similarity

# Streamlit App
def main():
    st.title("Profile JSON Generator, Comparison, and QR Code")

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

        # Save JSON file and optionally generate QR code
        if st.button("Save JSON and Generate QR Code"):
            filename = f"{name.replace(' ', '_').lower()}_data.json"
            filepath = save_json_file(data, filename)
            st.success(f"Data saved as {filepath}")

            qr_filename = f"{name.replace(' ', '_').lower()}_qr.png"
            qr_filepath = generate_qr_code(json.dumps(data), qr_filename)
            st.success(f"QR Code saved as {qr_filepath}")
            st.image(qr_filepath, caption="Generated QR Code")
            st.download_button("Download JSON", data=json.dumps(data, indent=4), file_name=filename, mime="application/json")

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
                        profile1[key] = []
                    if key not in profile2:
                        profile2[key] = []

                # Compare profiles and display the similarity percentage
                match_percentage = compare_profiles_ai(profile1, profile2)
                st.success(f"AI-based Match Percentage: {match_percentage:.2f}%")

            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload valid JSON files.")
            except ValueError as e:
                st.error(f"Error during comparison: {e}")

    elif choice == "Load JSON File to Generate QR Code":
        st.header("Load JSON File to Generate QR Code")
        uploaded_json_file = st.file_uploader("Upload a JSON file", type=["json"])
        
        if uploaded_json_file:
            try:
                json_data = json.load(uploaded_json_file)
                qr_filename = "uploaded_qr.png"
                qr_filepath = generate_qr_code(json.dumps(json_data), qr_filename)
                st.success("QR Code generated successfully!")
                st.image(qr_filepath, caption="Generated QR Code")
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON file.")

    elif choice == "Load and Decode QR Code":
        st.header("Load and Decode QR Code")
        st.write("Upload an image containing a QR code to decode its content.")

        uploaded_qr_file = st.file_uploader("Upload a QR Code Image", type=["png", "jpg", "jpeg"])
        
        if uploaded_qr_file:
            decoded_data = decode_qr_code(uploaded_qr_file)
            if "Error" in decoded_data:
                st.error(decoded_data)
            else:
                st.success("QR Code Decoded Successfully!")
                st.write(f"Decoded Data: {decoded_data}")


if __name__ == "__main__":
    main()