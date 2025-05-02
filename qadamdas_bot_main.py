# qadamdas_bot_main.py
# 1-бөлім: Telegram ботты іске қосу және сурет қабылдау

from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import logging
import os
from datetime import datetime
from ocr import extract_km_from_image
from sheets import add_entry_to_sheet, register_user, get_user_fullname

# 🔐 Бот токені (сенің токеніңді осында қой)
TELEGRAM_BOT_TOKEN = "7795779146:AAEpik_Z4AEnWZjQVdPOV9Uuq3WmcdKDhW8"

# 🔧 Лог баптауы
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 📌 Команда: /aty Атыңды енгіз
user_map = {}

def set_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    full_name = ' '.join(context.args)
    if not full_name:
        update.message.reply_text("Толық атыңызды енгізсеңіз жақсы болар еді. Мысалы: /aty Айгүл Қуанышқызы")
        return
    register_user(user_id, full_name, update.message.from_user.username)
    update.message.reply_text(
    f"Сәлеметсіз бе, Qadamdas марафонына қош келдіңіз!\n\n"
    f"Атыңызды сәтті тіркедік: {full_name}\n"
    "Енді жай ғана скриншот жіберсеңіз жеткілікті!"
)

# 📸 Фото қабылдау

def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    file_path = f"{user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    photo_file.download(file_path)

    # OCR арқылы қашықтықты шығару
    distance_km = extract_km_from_image(file_path)
    if not distance_km:
        update.message.reply_text("❗ Қашықтық табылмады. Скриншотта 'km' немесе 'км' болу керек.")
        os.remove(file_path)
        return

    # Sheets-ке жазу
    full_name = get_user_fullname(user.id)
    if not full_name:
        update.message.reply_text("Өтінеміз, алдымен /aty командасы арқылы толық атыңызды жазып жіберіңіз.")
        os.remove(file_path)
        return

    today = datetime.now().strftime("%d.%m.%Y")
    add_entry_to_sheet(full_name, user.username, today, distance_km)
    update.message.reply_text(f"✅ {distance_km} км тіркелді. Жарайсың, {full_name}!")
    os.remove(file_path)

# ▶️ Ботты іске қосу

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("aty", set_name))
    dp.add_handler(CommandHandler("atyn_ozgertu", set_name))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
