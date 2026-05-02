# ASHA Sahayi – Voice-Based Health Assistant Bot

##  Overview
ASHA Sahayi is a Telegram bot designed to assist ASHA workers in rural and semi-urban areas. It allows voice-based patient data entry, structured extraction, patient tracking, and safe medical advice.

---

##  Features

###  1. Voice Input (STT)
- Accepts voice messages via Telegram
- Converts speech to text using SpeechRecognition (Google STT)
- Supports multilingual and mixed-language inputs (Hindi-English, Telugu-English)

---

###  2. Structured Data Extraction
- Uses Gemini (schema-guided prompting) to extract:
  - Patient Name
  - Blood Pressure
  - Date
- Includes fallback rule-based extraction for robustness

---

###  3. State Management (Database)
- Uses SQLite to store patient records
- Recognizes recurring patients
- Displays previous records for context

---

###  4. RAG (Medical Advice)
- Uses predefined health guidelines (simulating NHM protocol)
- Avoids hallucinated AI responses using deterministic logic

---

##  System Architecture

Voice Input → STT → AI Extraction → Database → Retrieval → Advice Engine

---

##  Tech Stack

- Python  
- python-telegram-bot  
- SpeechRecognition  
- Gemini API  
- SQLite  
- pydub  

---

##  Error Handling

- Fallback extraction if AI fails  
- Handles unclear or missing input gracefully  

---

##  Language Support

- Supports English, Hindi-English, and Telugu-English inputs  
- Accuracy depends on speech recognition quality  

---

##  Ethical AI & Data Privacy

### Medical Safety
- The bot provides suggestions only and is not a replacement for professional medical advice  

### PII Protection
- Patient data is stored locally using SQLite  
- No external sharing of sensitive data  

### Consent
- Assumes ASHA workers have obtained necessary consent before logging patient data  

---

##  Future Improvements

- Full regional language support  
- Cloud database integration (Supabase/Firebase)  
- Advanced RAG using official health documents  

---

##  How to Run

1. Install dependencies:
```
pip install -r requirements.txt
```   
2. Add API keys in `.env` file:
```   
TELEGRAM_TOKEN=your_token
GEMINI_API_KEY=your_key
```
3. Run the bot: 
```
python bot.py
```

---

##  Demo

The bot can:
- Accept voice input  
- Extract patient data  
- Store and retrieve records  
- Provide medical advice  

---

##  Disclaimer

This bot is an assistant tool and not a substitute for professional medical diagnosis    