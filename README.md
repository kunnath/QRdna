# QRdna
# QR Code Generator and JSON Saver

## Overview
This application allows users to create and share their personal information via QR codes and JSON files. With a simple interface, users can:
- Enter personal details and habits.
- Generate a QR code for their data.
- Save their information as a JSON file.
- Upload an existing JSON file to generate a QR code.

Built using **Streamlit**, this tool simplifies contact sharing and habit tracking, making it a useful resource for personal or professional use.

---

## Features

### 1. Save JSON File
- Input personal details and save them as a JSON file for reuse.
- Files are saved dynamically with user-specific names in the `saved_data` directory.

### 2. Generate QR Code
- Create a QR code from the entered data or an uploaded JSON file.
- QR codes can be downloaded and shared with others.

### 3. Load JSON File
- Upload an existing JSON file to regenerate the QR code.

---

## Installation

### Prerequisites
- Python 3.7 or higher

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/qr-code-app.git
   cd qr-code-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage

### Step 1: Launch the App
Run the app and open it in your browser using the URL provided by Streamlit (e.g., `http://localhost:8501`).

### Step 2: Enter Your Information
- Fill out the input fields with your personal details and habits.
- Click **"Save JSON and Generate QR Code"** to save the data and generate a QR code.

### Step 3: Download Files
- Download the generated QR code and JSON file.

### Step 4: Load JSON File (Optional)
- Upload a previously saved JSON file to regenerate its QR code.

---

## File Structure
```
qr-code-app/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── saved_data/           # Directory for saving JSON files
├── README.md             # Documentation
```

---

## Dependencies
- **Streamlit**: For the web interface
- **qrcode**: For generating QR codes
- **Pillow**: For handling image files

Install them using:
```bash
pip install streamlit qrcode pillow
```

---

## Contribution
Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For questions or support, contact:
- **Name**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [Your GitHub](https://github.com/your-username)

