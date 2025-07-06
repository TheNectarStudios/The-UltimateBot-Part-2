import os
from upload import upload_video

def run_upload():
    print("🚀 Starting YouTube Shorts upload process...")

    title = "Awesome Naruto AMV #Shorts"
    description = "Auto-generated Naruto AMV Shorts. Like & Subscribe! 🍥"
    tags = ["Naruto", "AMV", "Shorts", "Anime"]

    # This must match what you set as FINAL_VIDEO in your main script:
    video_file_path = "short_final.mp4"

    if not os.path.exists(video_file_path):
        print(f"❌ Final video not found: {video_file_path}")
        return

    upload_video(title, description, tags, video_file=video_file_path)

if __name__ == "__main__":
    run_upload()
