import os
import json
from upload import upload_video

def run_upload():
    print("🚀 Starting YouTube Shorts upload process...")

    script_path = "assets/scripts/latest_script.json"
    if not os.path.exists(script_path):
        print("❌ Script JSON not found.")
        return

    with open(script_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Epic AMV #Shorts")
    description = data.get("description", "")
    tags = data.get("tags", [])

    video_file_path = "short_final.mp4"
    if not os.path.exists(video_file_path):
        print(f"❌ Final video not found: {video_file_path}")
        return

    upload_video(title, description, tags, video_file=video_file_path)
