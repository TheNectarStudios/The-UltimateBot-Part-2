import os
import openai
import json
import re
from dotenv import load_dotenv

# 🔐 Load OpenRouter API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"Generate YouTube Shorts metadata for this anime AMV topic: '{topic}'.\n\n"
        "🎬 TASK:\n"
        "- Suggest a short, catchy YouTube title (max 80 chars)\n"
        "- Write a 3–4 line description highlighting the anime/music mix\n"
        "- Include 7–10 relevant tags (anime names, music name, 'AMV', etc)\n"
        "- Mood: Suggest one-word background music mood (e.g., emotional, hype, sad, epic)\n\n"
        "✨ FORMAT (Return as JSON):\n"
        "{\n"
        "  \"title\": \"<video title>\",\n"
        "  \"description\": \"<video description>\",\n"
        "  \"tags\": [\"Naruto\", \"AMV\", ...],\n"
        "  \"mood\": \"emotional\"\n"
        "}\n\n"
        "✅ Notes:\n"
        "- Be relevant to the query\n"
        "- No hashtags in tags list\n"
        "- Keep it concise, high quality\n\n"
        "Return raw JSON only. No explanation or commentary."
    )

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a metadata generator for anime YouTube Shorts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
        )

        raw = response['choices'][0]['message']['content'].strip()
        print("🪵 RAW RESPONSE:\n", raw)

        # Extract the first full JSON block
        match = re.search(r"\{[\s\S]+?\}", raw)
        if not match:
            print("⚠️ No valid JSON object found.")
            return None

        cleaned_json = match.group(0)

        # Fix common issues
        cleaned_json = re.sub(r",\s*([}\]])", r"\1", cleaned_json)  # remove trailing commas
        cleaned_json = cleaned_json.replace("“", "\"").replace("”", "\"")
        cleaned_json = cleaned_json.replace("‘", "'").replace("’", "'")

        data = json.loads(cleaned_json)

        # Save to file
        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n📝 Title: {data.get('title')}")
        print(f"📝 Description: {data.get('description')}")
        print(f"🏷️ Tags: {data.get('tags')}")
        print(f"🎵 Mood: {data.get('mood')}")

        return data

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
