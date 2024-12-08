# QRdna: QR Code Generator and JSON Saver

## Overview
QRdna is a user-friendly application built with Streamlit that allows you to create and share your personal information through QR codes and JSON files. Whether you’re sharing contact details or tracking habits, QRdna simplifies the process with an easy-to-use interface.

### Key Features
1. **Save JSON File**
   - Enter your personal details and habits and save them as a JSON file for later use.
   - Files are automatically saved with unique user-specific names in the `saved_data` directory.

2. **Generate QR Code**
   - Create a QR code from your entered data or an uploaded JSON file.
   - Download and share QR codes seamlessly.

3. **Load JSON File**
   - Upload an existing JSON file to regenerate the corresponding QR code.

## Installation
### Prerequisites
Ensure that you have Python 3.7 or higher installed on your system.

### Steps to Install and Run
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/qr-code-app.git
   cd qr-code-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage
### Step 1: Launch the App
Run the app with the command provided and open it in your web browser using the URL shown by Streamlit (e.g., [http://localhost:8501](http://localhost:8501)).

### Step 2: Enter Your Information
- Fill out the input fields with your personal details and habits.
- Click "Save JSON and Generate QR Code" to save your data and create a QR code.

### Step 3: Download Files
- Download your generated QR code and the JSON file for sharing or future use.

### Step 4: Load JSON File (Optional)
- Upload a previously saved JSON file to regenerate its QR code.

## File Structure
```plaintext
qr-code-app/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── saved_data/           # Directory for saving JSON files
├── README.md             # Documentation
```  

## Dependencies
Ensure that you have the following packages installed:
- **Streamlit**: For building the web interface.
- **qrcode**: For generating QR codes.
- **Pillow**: For handling image files.

You can install all dependencies by running:
```bash
pip install streamlit qrcode pillow
```

## Docker Setup
### Build the Docker Image
```bash
docker build -t streamlit-app .
```

### Run the Docker Container
```bash
docker run -p 8501:8501 streamlit-app
```

## Contribution
Contributions are highly welcome! Feel free to:
- Report bugs.
- Suggest new features.
- Submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, reach out to:
- **Name**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [Your GitHub](https://github.com/your-username)

We hope you find QRdna a helpful tool for sharing and managing your contact information and habits!

