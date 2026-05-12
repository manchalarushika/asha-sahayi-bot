# ASHA Sahayi – Voice-Based Health Assistant Bot

## Overview
ASHA Sahayi is a Telegram bot designed to assist ASHA workers in rural and semi-urban areas. It allows voice-based patient data entry, structured extraction, patient tracking, and safe medical advice. The system uses an external guideline file (guidelines.txt) for medical advice retrieval.

---

## Features

### 1. Voice Input (STT)
- Accepts voice messages via Telegram
- Converts speech to text using SpeechRecognition (Google STT)
- Supports multilingual and mixed-language inputs (Hindi-English, Telugu-English)

---

### 2. Structured Data Extraction
- Uses Gemini-based schema-guided prompting with rule-based fallback extraction to extract:
  - Patient Name
  - Blood Pressure
  - Date
- Includes fallback rule-based extraction for robustness

---

### 3. State Management (Database)
- Uses SQLite to store patient records
- Recognizes recurring patients
- Displays previous records for context

---

### 4. RAG (Retrieval-Augmented Generation)
- Uses a guideline document (`guidelines.txt`) as a trusted medical knowledge source
- Retrieves the relevant guideline section based on patient BP values
- Passes retrieved guideline context to the advice generation pipeline
- Produces guideline-grounded responses instead of relying only on hardcoded logic
- Includes fallback guideline-based advice generation for robustness

### 5. Ethical Consent Flow
- Displays a first-use consent message
- Requires `/consent` before processing or storing patient information
- Reinforces responsible handling of sensitive healthcare data

---

## System Architecture

Voice Input → STT → AI Extraction → Consent Validation → Database → Guideline Retrieval → Advice Engine

The system combines AI-based extraction with rule-based fallback and guideline-based retrieval for robust and safe operation.

---

## Tech Stack

- Python  
- python-telegram-bot  
- SpeechRecognition  
- Gemini API  
- SQLite  
- pydub  

---

## Error Handling

- Fallback extraction if AI fails  
- Handles unclear or missing input gracefully
- Hybrid system (AI + rule-based fallback) ensures reliability even if AI fails  

---

## Language Support

- Supports English, Hindi-English, and Telugu-English inputs  
- Accuracy depends on speech recognition quality  

---

## Ethical AI & Data Privacy

### Medical Safety
- The bot provides suggestions only and is not a replacement for professional medical advice  

### PII Protection
- Patient data is stored locally using SQLite  
- No external sharing of sensitive data  

### Consent
- The bot includes an in-app consent mechanism before any patient data is processed or stored
- Users must provide consent using the `/consent` command
- A warm first-use message informs users about data handling and storage  

---

## Future Improvements

- Full regional language support  
- Cloud database integration (Supabase/Firebase)  
- Advanced semantic RAG using official healthcare protocols and vector retrieval  

---

## How to Run

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

## Demo

The bot can:
- Accept voice input  
- Extract patient data  
- Store and retrieve records  
- Provide medical advice  

---

## Disclaimer

This bot is an assistant tool and not a substitute for professional medical diagnosis.   
