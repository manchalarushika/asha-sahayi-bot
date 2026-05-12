import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from ai_logic import speech_to_text, extract_patient_data, fallback_extraction
from db import insert_patient, get_patient_history
from ai_logic import get_medical_advice
from ai_logic import get_rag_advice
from telegram.ext import CommandHandler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
user_consent = {}
async def consent(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    user_consent[user_id] = True

    await update.message.reply_text(
        " Thank you. Consent received.\n"
        "Patient data will now be stored securely."
    )

#  TEXT FUNCTION
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in user_consent:

        await update.message.reply_text(
            " Namaste 🙏\n"
            "This bot stores patient details only with your consent.\n"
            "Please type /consent before using the bot."
        )
        return

    text = update.message.text
    await update.message.reply_text(f"You said: {text}")


#  VOICE FUNCTION
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_consent:

        await update.message.reply_text(
            " Namaste 🙏\n"
            "This bot stores patient details only with your consent.\n"
            "Please type /consent before using the bot."
        )
        return
    voice = await update.message.voice.get_file()
    
    file_path = "voice.ogg"
    await voice.download_to_drive(file_path)

    await update.message.reply_text("Processing voice...")

    text = speech_to_text(file_path)
    await update.message.reply_text(f"Text: {text}")

    #  AI extraction
    data = extract_patient_data(text)

    #  fallback if AI fails
    if data.get("name") == "" and data.get("blood_pressure") == "":
        data = fallback_extraction(text)

    #  Output
    await update.message.reply_text(
        f" Patient Data:\n"
        f"Name: {data.get('name','')}\n"
        f"BP: {data.get('blood_pressure','')}\n"
        f"Date: {data.get('date','')}"
    )
    #  Get medical advice
    advice = get_rag_advice(data.get("blood_pressure"))
    await update.message.reply_text(advice)
    #  Check previous record
    old_records = get_patient_history(data.get("name"))

    if old_records:
        msg = " Previous Records:\n"
        for rec in old_records:
            msg += f"Name: {rec[0]}, BP: {rec[1]}, Date: {rec[2]}\n"
        await update.message.reply_text(msg)

    #  Save new data
    insert_patient(
        data.get("name"),
        data.get("blood_pressure"),
        data.get("date")
    )

    await update.message.reply_text(" Data saved successfully")

# BOT SETUP
# BOT SETUP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("consent", consent))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

print("Bot is running...")
app.run_polling()
