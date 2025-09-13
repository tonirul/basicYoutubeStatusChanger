# 📺 YouTube Private Video Updater (CLI)

This is a **Python command-line script** that finds all your **private YouTube videos** and updates them to **unlisted** using the **YouTube Data API v3**.  

Unlike the Flask web version, this runs directly in your **terminal/command prompt**.

---

## 🚀 Features
- Authenticate with Google (OAuth2, local browser login)
- Fetch your **Uploads playlist**
- Detect **private videos**
- Update them to **unlisted**
- Safe **daily limit (200 videos per run)** to avoid quota issues
- Console logs show progress (with ✅ and ⚠️ symbols)

---

## 🛠️ Requirements
- Python **3.8+**
- Google Cloud Project with **YouTube Data API v3** enabled
- OAuth2 credentials file (`client_secret.json`)

---

## 📂 Project Files
.
├── updater.py # The script (your code above)
├── client_secret.json # OAuth2 credentials (from Google Cloud)
├── token.pickle # Auto-created after login (stores your session)

yaml


---

## 📦 Installation

1. **Clone / download** this project:

```bash
git clone https://github.com/yourusername/youtube-private-updater-cli.git
cd youtube-private-updater-cli
Create a virtual environment (optional, recommended):

bash

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
Install dependencies:

bash

pip install google-api-python-client google-auth google-auth-oauthlib
(Or add them in requirements.txt and run pip install -r requirements.txt)

🔑 Setup Google API Credentials
Go to Google Cloud Console

Create a new project (or use an existing one)

Enable YouTube Data API v3

Go to APIs & Services → Credentials

Create OAuth Client ID → Select Desktop App

Download the JSON file

Rename it to client_secret.json and place it in this folder

⚠️ Never share client_secret.json or token.pickle publicly.

▶️ Usage
Run the script:

bash

python updater.py
On first run, a browser window will open for Google login.

Allow permissions for YouTube Data API v3.

A token.pickle file will be saved for future runs.

The script will:

Fetch your uploads

Detect private videos

Update them to unlisted

Show progress in the terminal

Example output:

vbnet

✅ Connected to YouTube API
📂 Uploads Playlist ID: UUabc123xyz
📄 Fetching page 1 of uploads...
   ➡️ Found 50 items on this page
   🔒 Found private video: abc123
✅ Updated Video ID: abc123 → UNLISTED (1/200)
...
⏹️ Stopped — daily limit reached (200). Run again tomorrow for the next batch.
⚙️ Configuration
Default daily update limit: 200 videos

You can change this by editing the constant in the script:

python

DAILY_LIMIT = 200
🧹 Resetting Login
To re-authenticate with Google, delete token.pickle:

bash

rm token.pickle
Next time you run the script, it will ask you to log in again.

⚠️ Notes
Works only on your own YouTube channel (requires OAuth login).

Do not exceed YouTube API quota limits.

For large libraries, re-run daily until all videos are processed.

📜 License
This project is for personal use only.
Must comply with YouTube API Terms of Service.
