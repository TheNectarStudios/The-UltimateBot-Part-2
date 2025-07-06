import os
from upload import upload_video

def run_upload():
    print("🚀 Starting YouTube Shorts upload process...")

    # 🗒️ Try to read original downloaded title
    base_title = "Awesome Naruto AMV"
    title_file = "video_title.txt"

    if os.path.exists(title_file):
        with open(title_file, "r", encoding="utf-8") as f:
            file_title = f.read().strip()
            if file_title:
                base_title = file_title
                print(f"✅ Loaded original video title: {base_title}")
            else:
                print("⚠️ video_title.txt is empty. Using default title.")
    else:
        print(f"⚠️ {title_file} not found. Using default title.")

    # 🎯 Final YouTube title and description
    title = f"{base_title} | Naruto AMV #Shorts"
    description = (
        f"Watch this epic Naruto AMV: '{base_title}'!\n"
        "Auto-edited and uploaded by my Python bot. Like & Subscribe for more! 🍥🔥\n"
        "#Naruto #AMV #Shorts #Anime"
    )
    tags = ["Naruto", "AMV", "Shorts", "Anime"]

    # ✅ This should match your output video name
    video_file_path = "short_final.mp4"

    if not os.path.exists(video_file_path):
        print(f"❌ Final video not found: {video_file_path}")
        return

    # 📡 Upload it!
    upload_video(title, description, tags, video_file=video_file_path)

if __name__ == "__main__":
    run_upload()
