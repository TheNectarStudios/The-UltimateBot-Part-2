import os
from video_extractor import extract_video
from generate_script import generate_youtube_script
from upload import upload_video

def main():
    print("🎯 Welcome to the AMV Shorts Bot!")

    # Step 1: User Input
    query = input("🔎 Enter anime/music combo to search: ").strip()
    if not query:
        print("❌ Empty input! Exiting.")
        return

    # Step 2: Extract video (download + resize)
    try:
        print("\n📽️ Extracting video...")
        _, video_path = extract_video(query)
    except Exception as e:
        print(f"❌ Video extraction failed: {e}")
        return

    # Step 3: Generate metadata from prompt
    print("\n🧠 Generating title, description, and tags from query...")
    metadata = generate_youtube_script(query)
    if not metadata:
        print("❌ Metadata generation failed.")
        return

    title = metadata["title"]
    description = metadata["description"]
    tags = metadata["tags"]

    # Step 4: Upload to YouTube
    print("\n🚀 Uploading to YouTube Shorts...")
    upload_video(title, description, tags, video_file=video_path)

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
