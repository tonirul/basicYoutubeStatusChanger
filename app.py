from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import time

# Scopes required for managing YouTube videos
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Daily safe update limit
DAILY_LIMIT = 200

def get_authenticated_service():
    """Authenticate and return YouTube API client"""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def get_uploads_playlist_id(youtube):
    """Get the channel’s Uploads playlist ID"""
    request = youtube.channels().list(
        part="contentDetails",
        mine=True
    )
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def list_private_videos(youtube, uploads_playlist_id, limit=DAILY_LIMIT):
    """Fetch up to `limit` private videos from uploads playlist"""
    videos = []
    next_page_token = None
    page = 1

    while True:
        print(f"📄 Fetching page {page} of uploads...")

        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        items = response.get("items", [])
        print(f"   ➡️ Found {len(items)} items on this page")

        video_ids = [item["contentDetails"]["videoId"] for item in items]

        if video_ids:
            video_request = youtube.videos().list(
                part="id,status",
                id=",".join(video_ids)
            )
            video_response = video_request.execute()

            for item in video_response.get("items", []):
                status = item["status"]
                if status.get("privacyStatus") == "private":
                    print(f"   🔒 Found private video: {item['id']}")
                    videos.append(item["id"])
                    if len(videos) >= limit:
                        print(f"✅ Reached daily limit of {limit} private videos.")
                        return videos

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            print("✅ No more pages left.")
            break

        page += 1

    return videos

def update_videos_to_unlisted(youtube, video_ids):
    """Change given private videos to unlisted"""
    count = 0
    for vid in video_ids:
        try:
            request = youtube.videos().update(
                part="status",
                body={
                    "id": vid,
                    "status": {
                        "privacyStatus": "unlisted"
                    }
                }
            )
            response = request.execute()
            count += 1
            print(f"✅ Updated Video ID: {vid} → UNLISTED ({count}/{DAILY_LIMIT})")
            time.sleep(0.1)  # slight delay to be safe
        except Exception as e:
            print(f"⚠️ Error updating {vid}: {e}")
        if count >= DAILY_LIMIT:
            print("⏹️ Stopped — daily limit reached (200). Run again tomorrow for the next batch.")
            break

def main():
    youtube = get_authenticated_service()
    print("✅ Connected to YouTube API")

    uploads_playlist_id = get_uploads_playlist_id(youtube)
    print(f"📂 Uploads Playlist ID: {uploads_playlist_id}")

    private_videos = list_private_videos(youtube, uploads_playlist_id, limit=DAILY_LIMIT)
    print(f"🔍 Found {len(private_videos)} private videos (processing up to {DAILY_LIMIT})")

    if not private_videos:
        print("ℹ️ No private videos found. Nothing to update.")
    else:
        update_videos_to_unlisted(youtube, private_videos)

if __name__ == "__main__":
    main()
