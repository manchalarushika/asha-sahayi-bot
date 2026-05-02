import speech_recognition as sr
from pydub import AudioSegment

# 🔹 Gemini setup
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")


# ✅ STEP 1: Voice → Text
def speech_to_text(file_path):
    sound = AudioSegment.from_ogg(file_path)
    sound.export("voice.wav", format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile("voice.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return "Sorry, could not understand audio"


# ✅ STEP 2: AI-based extraction (schema guided)
def extract_patient_data(text):
    prompt = f"""
    Extract patient details from the text and return ONLY valid JSON.

    Do NOT add explanation.
    Do NOT use markdown.

    JSON format:
    {{
      "name": "",
      "blood_pressure": "",
      "date": ""
    }}

    Text: {text}
    """

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()

        result = result.replace("```json", "").replace("```", "").strip()

        data = json.loads(result)
        return data

    except:
        return {
            "name": "",
            "blood_pressure": "",
            "date": ""
        }
def extract_name(text):
    words = text.split()

    for i, word in enumerate(words):
        if "bp" in word.lower():

            # Case 1: word before BP
            if i > 0 and words[i-1][0].isupper():
                return words[i-1]

            # Case 2: "for Radha"
            if i < len(words) - 2:
                if words[i+1].lower() == "for" and words[i+2][0].isupper():
                    return words[i+2]

    # fallback: first capital word
    for word in words:
        if word[0].isupper():
            return word

    return ""

# ✅ STEP 3: Fallback extraction (for robustness)
def fallback_extraction(text):
    data = {
        "name": "",
        "blood_pressure": "",
        "date": ""
    }

    text_lower = text.lower()
    words = text.split()

    # BP extraction
    bp_match = re.search(r"(\d{2,3})\s*(/|by)\s*(\d{2,3})", text_lower)
    if bp_match:
        data["blood_pressure"] = f"{bp_match.group(1)}/{bp_match.group(3)}"

    # Name extraction
    # Try first word
    data["name"] = extract_name(text)

    # Date extraction
    if "today" in text_lower:
        data["date"] = "today"
    else:
        data["date"] = datetime.now().strftime("%Y-%m-%d")

    return data

def get_medical_advice(bp):
    if not bp:
        return "No BP data available"

    try:
        systolic = int(bp.split("/")[0])

        if systolic >= 140:
            return "⚠️ High BP. Please consult a doctor."
        elif 120 <= systolic < 140:
            return "🟡 Slightly elevated BP. Monitor regularly."
        else:
            return "🟢 BP is normal. Maintain healthy lifestyle."

    except:
        return "Unable to analyze BP"