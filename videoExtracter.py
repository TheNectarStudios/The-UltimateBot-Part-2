import os
from googleapiclient.discovery import build
import yt_dlp
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize
from moviepy.video.fx.crop import crop
from dotenv import load_dotenv

# 📥 Load API key from .env
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise Exception("❌ Missing YOUTUBE_API_KEY in .env file!")

# 🎯 Search & download settings
SEARCH_QUERY = "Naruto AMV"
OUTPUT_FOLDER = "downloads"
FINAL_VIDEO = "short_final.mp4"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def search_valid_amv(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        videoDuration="medium",  # Excludes Shorts
        maxResults=10
    )
    response = request.execute()

    video_links = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"🔍 Found: {title}")
        video_links.append(url)

    return video_links

def download_first_valid_video(video_urls, output_dir):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "downloaded.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        # 🪄 👇 ABSOLUTE FFmpeg path fix!
        "ffmpeg_location": r"C:\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
    }

    for url in video_urls:
        try:
            print(f"📥 Downloading: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                duration = info.get("duration", 0)
                if duration >= 120:
                    print("✅ Video meets length requirement.")
                    return os.path.join(output_dir, "downloaded.mp4")
                else:
                    print("⏱️ Skipped (under 2 mins).")
        except Exception as e:
            print(f"⚠️ Failed to download: {e}")

    raise Exception("❌ No valid AMV found or all too short.")

def convert_to_shorts_format(input_path, output_path):
    print("🎞️ Converting to Shorts format...")
    clip = VideoFileClip(input_path).subclip(0, 60)  # First 60 seconds

    # Shorts resolution (9:16) — portrait
    target_height = 1920
    target_width = 1080
    clip = resize(clip, height=target_height)

    if clip.w < target_width:
        delta = (target_width - clip.w) // 2
        clip = clip.margin(left=delta, right=delta, color=(0, 0, 0))
    elif clip.w > target_width:
        clip = crop(clip, x_center=clip.w / 2, width=target_width)

    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"✅ Final Shorts video saved as: {output_path}")

if __name__ == "__main__":
    print(f"🔍 Searching YouTube for: {SEARCH_QUERY}")
    links = search_valid_amv(SEARCH_QUERY)

    print(f"\n📥 Downloading first valid video...")
    downloaded_path = download_first_valid_video(links, OUTPUT_FOLDER)

    print(f"\n🎬 Editing video...")
    convert_to_shorts_format(downloaded_path, FINAL_VIDEO)
