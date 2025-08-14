Follow these steps to set up and run the Speech Transcriber app on your computer.

---
✅ STEP 1: Install Python

- Download Python from: https://www.python.org/downloads/
- During installation, make sure to check the box that says:
   "Add Python to PATH"
---

✅ STEP 2: Install Required Packages

- Open Command Prompt 
- Navigate to the folder where you extracted the app
- Run the following command to install all required packages:
  > python -m pip install -r requirements.txt
---

✅ STEP 3: Install FFmpeg
- Download FFmpeg from this link:
  🔗 https://www.gyan.dev/ffmpeg/builds/

- Choose the version under "Release builds" → click "ffmpeg-release-essentials.zip"
- Extract the zip file
- Copy the path to the `bin` folder inside the extracted folder
 
- Add this path to your System Environment Variables:
  1. Search for "Environment Variables" in Windows
  2. Click "Edit the system environment variables"
  3. Click "Environment Variables"
  4. Under "System variables", find `Path` and click "Edit"
  5. Click "New" and paste the path to the `bin` folder
  6. Click OK to save

---

✅ STEP 4: Run the App

- Double-click the file named:
  > Start Transcriber.bat

- This will launch the app in your browser using Streamlit

---

