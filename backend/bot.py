import os
import telebot
from dotenv import load_dotenv
from telebot import apihelper
from backend.converter import convert_to_wav # ប្រើប្រាស់ឈ្មោះមុខងារថ្មី

apihelper.READ_TIMEOUT = 90

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តី! 👋 សូមផ្ញើឯកសារ MP3 ឬ គ្រាន់តែចុច Record សារសំឡេងមកកាន់ខ្ញុំ ខ្ញុំនឹងបម្លែងវាទៅជា WAV ជូនអ្នកភ្លាមៗ។")

# ⚠️ ចំណុចផ្លាស់ប្តូរទី ១៖ បន្ថែម 'voice' ទៅក្នុងបញ្ជី
@bot.message_handler(content_types=['audio', 'document', 'voice'])
def handle_audio_files(message):
    try:
        bot.reply_to(message, "📥 ទទួលបានឯកសារ! កំពុងដំណើរការបម្លែង សូមរង់ចាំបន្តិច...")
        
        # ⚠️ ចំណុចផ្លាស់ប្តូរទី ២៖ ចាប់យក Voice Message និងផ្តល់ឈ្មោះឲ្យវា
        if message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            original_name = "voice_record.ogg"
        elif message.content_type == 'audio':
            file_info = bot.get_file(message.audio.file_id)
            original_name = message.audio.file_name or "audio.mp3"
        else:
            file_info = bot.get_file(message.document.file_id)
            original_name = message.document.file_name or "document.mp3"

        # កំណត់ឈ្មោះឯកសារបណ្តោះអាសន្ន
        input_path = f"temp_{original_name}"
        # ដូរទាំងកន្ទុយ .mp3 និង .ogg ទៅជា .wav
        output_name = original_name.replace('.mp3', '.wav').replace('.ogg', '.wav')
        output_path = f"converted_{output_name}"

        # ទាញយកឯកសារពី Telegram
        downloaded_file = bot.download_file(file_info.file_path)
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # ដំណើរការបម្លែង 
        success = convert_to_wav(input_path, output_path)

        if success:
            with open(output_path, 'rb') as audio_to_send:
                bot.send_audio(message.chat.id, audio_to_send, title="Converted to WAV")
            bot.send_message(message.chat.id, "✅ ការបម្លែងទទួលបានជោគជ័យ!")
        else:
            bot.send_message(message.chat.id, "❌ សុំទោស មានបញ្ហាក្នុងការបម្លែង។")

        # លុបឯកសារបណ្តោះអាសន្នចេញ
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

    except Exception as e:
        bot.reply_to(message, f"❌ មានបញ្ហាបច្ចេកទេស៖ {e}")

print("🤖 Bot កំពុងដំណើរការ... ចុច Ctrl+C ដើម្បីបញ្ឈប់។")
bot.infinity_polling()