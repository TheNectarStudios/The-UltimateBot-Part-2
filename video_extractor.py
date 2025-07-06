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

# 🎯 Setup
OUTPUT_FOLDER = "downloads"
FINAL_VIDEO = "short_final.mp4"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_video(search_query):
    print(f"\n🔍 Searching YouTube for: {search_query}")
    links = search_valid_amv(search_query)

    print(f"\n📥 Downloading first valid video...")
    downloaded_path, title = download_first_valid_video(links, OUTPUT_FOLDER)

    print(f"\n🎬 Editing video...")
    convert_to_shorts_format(downloaded_path, FINAL_VIDEO)

    return title, FINAL_VIDEO

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
        "ffmpeg_location": r"C:\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"  # ⚠️ Change path if needed
    }

    for url in video_urls:
        try:
            print(f"📥 Downloading: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                duration = info.get("duration", 0)
                if duration >= 120:
                    print("✅ Video meets length requirement.")
                    return os.path.join(output_dir, "downloaded.mp4"), info.get("title", url)
                else:
                    print("⏱️ Skipped (under 2 mins).")
        except Exception as e:
            print(f"⚠️ Failed to download: {e}")

    raise Exception("❌ No valid AMV found or all too short.")

def convert_to_shorts_format(input_path, output_path):
    print("🎞️ Converting to Shorts format (last 30s)...")

    clip = VideoFileClip(input_path)
    actual_duration = clip.duration

    end = actual_duration - 0.5  # ensure no out-of-bounds
    start = max(end - 30, 0)

    print(f"🎞️ Using subclip from {start:.2f}s to {end:.2f}s (of {actual_duration:.2f}s total)")
    subclip = clip.subclip(start, end)

    # Resize to vertical 1080x1920
    target_height = 1920
    target_width = 1080
    subclip = resize(subclip, height=target_height)

    if subclip.w < target_width:
        delta = (target_width - subclip.w) // 2
        subclip = subclip.margin(left=delta, right=delta, color=(0, 0, 0))
    elif subclip.w > target_width:
        subclip = crop(subclip, x_center=subclip.w / 2, width=target_width)

    subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"✅ Final Shorts video saved as: {output_path}")
