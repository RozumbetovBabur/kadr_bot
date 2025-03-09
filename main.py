from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext,CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton,Document, PhotoSize, BotCommand
import sqlite3
from Dictionaries import TEXTS  # Dictionaries.py faylidan matnlarni import qilamiz

TOKEN = "TOKEN"
GROUP_CHAT_ID = ID


# Hujjatlarni vaqtincha saqlash uchun lug‘at
user_documents = {}

# Foydalanuvchi bosqichlari
CHOOSE_LANGUAGE, CHOOSE_LANGUAGE_UPDATE, ASK_NAME, ASK_SURNAME, ASK_PHONE, MAIN_MENU = range(6)
ASK_CV, ASK_DIPLOM, ASK_CERTIFICATE, WAIT_FOR_CERTIFICATE_UPLOAD = range(4)

# 📌 SQLite3 bazasini yaratish
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    language INTEGER DEFAULT 2
)
""")
conn.commit()


def set_bot_commands(bot):
    """Botga buyruqlarni o‘rnatish"""
    commands = [
        BotCommand("start", "Ботни ишга тушириш / Запустить бота")

    ]
    bot.set_my_commands(commands)  # ✅ TO‘G‘RI: `bot` obyektini ishlatish kerak



# 🏁 /start komandasi - til tanlash
def start_handler(update, context):
    user_id = update.message.from_user.id

    # 📌 Foydalanuvchi bazada bormi yoki yo‘qmi?
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        lang_id = user_data[0]  # Foydalanuvchining saqlangan tili
        update.message.reply_text(TEXTS["registered"][lang_id])  # "Siz ro‘yxatdan o‘tgansiz!"
        return show_main_menu(update, context)
    else:
        buttons = [
            ["🇰🇿 Qaraqalpaq tili", "🇺🇿 O‘zbek tili"],
            ["🇷🇺 Русский язык"]
        ]
        update.message.reply_text(TEXTS["start"][2],  # Standart O‘zbek tili
                                  reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return CHOOSE_LANGUAGE


def show_profile(update, context):
    user_id = update.message.from_user.id

    # 📌 Foydalanuvchining tilini bazadan olish
    cursor.execute("SELECT first_name, last_name, phone, language FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        first_name, last_name, phone, lang_id = user_data
        context.user_data["language"] = lang_id  # 🔹 `context.user_data` ga yozamiz
        update.message.reply_text(TEXTS["profile"][lang_id].format(first_name=first_name, last_name=last_name, phone=phone))
    else:
        update.message.reply_text("⚠️ Profil topilmadi! Iltimos, /start ni bosib ro‘yxatdan o‘ting.")


# ✅ Ismni olish
def get_name(update, context):
    context.user_data["first_name"] = update.message.text
    lang_id = context.user_data["language"]
    update.message.reply_text(TEXTS["ask_surname"][lang_id])
    return ASK_SURNAME

# ✅ Familiyani olish
def get_surname(update, context):
    context.user_data["last_name"] = update.message.text
    lang_id = context.user_data["language"]
    update.message.reply_text(TEXTS["ask_phone"][lang_id],
                              reply_markup=ReplyKeyboardMarkup(
                                  [[KeyboardButton(TEXTS["phone"][lang_id], request_contact=True)]],
                                  resize_keyboard=True, one_time_keyboard=True))
    return ASK_PHONE

# ✅ Telefon raqamini olish
def get_phone(update, context):
    user = update.message.from_user
    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    context.user_data["phone"] = phone_number
    lang_id = context.user_data["language"]

    cursor.execute("INSERT OR REPLACE INTO users (user_id, first_name, last_name, phone, language) VALUES (?, ?, ?, ?, ?)",
                   (user.id, context.user_data["first_name"], context.user_data["last_name"], phone_number, lang_id))
    conn.commit()

    return show_main_menu(update, context)

# 📌 Profilni ko‘rsatish
def show_profile(update, context):
    user_id = update.message.from_user.id

    # 📌 Foydalanuvchining ma’lumotlarini bazadan olish
    cursor.execute("SELECT first_name, last_name, phone, language FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        first_name, last_name, phone, lang_id = user_data

        # 🔹 Agar `context.user_data["language"]` bo‘lmasa, bazadan olinadi
        if "language" not in context.user_data:
            context.user_data["language"] = lang_id  # Tilni saqlash

        # 🔹 Profilni chiqarish
        update.message.reply_text(TEXTS["profile"][context.user_data["language"]].format(
            first_name=first_name, last_name=last_name, phone=phone
        ))
    else:
        update.message.reply_text("⚠️ Profil topilmadi! Iltimos, /start ni bosib ro‘yxatdan o‘ting.")


# 🔘 Asosiy menyuni chiqarish
def show_main_menu(update, context):
    user_id = update.message.from_user.id

    # 📌 Foydalanuvchining tilini bazadan olish
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        lang_id = user_data[0]  # Foydalanuvchining saqlangan tili
    else:
        lang_id = 2  # Agar til mavjud bo‘lmasa, standart O‘zbek tilini qo‘llaymiz

    buttons = [
        [TEXTS["profile_btn"][lang_id], TEXTS["jobs_btn"][lang_id]],  # Profil va Ishga hujjat jo‘natish
        [TEXTS["change_lang"][lang_id]]  # Tilni o‘zgartirish
    ]
    update.message.reply_text(TEXTS["main_menu"][lang_id],
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return MAIN_MENU

# Menyudagi tugmalarga javob beruvchi funksiya
def handle_main_menu(update, context):
    """Foydalanuvchi menyudagi tugmalarni bossa, mos funksiyaga yo‘naltiradi"""
    user_response = update.message.text
    user_id = update.message.from_user.id

    # 📌 Foydalanuvchining tilini bazadan olish
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        lang_id = user_data[0]  # Foydalanuvchining saqlangan tili
    else:
        lang_id = 2  # Agar til mavjud bo‘lmasa, standart O‘zbek tilini qo‘llaymiz

    if user_response == TEXTS["jobs_btn"][lang_id]:
        return send_document(update, context)  # Ishga hujjat jo‘natish funksiyasini chaqiramiz
    elif user_response == TEXTS["profile_btn"][lang_id]:
        return show_profile(update, context)  # Profilni ko‘rsatish funksiyasi
    elif user_response == TEXTS["change_lang"][lang_id]:
        return change_language(update, context)  # Tilni o‘zgartirish funksiyasi

    # Agar tugmalar orasida bo‘lmasa, foydalanuvchini asosiy menyuga qaytaramiz
    update.message.reply_text(TEXTS["invalid_option"][lang_id])
    return show_main_menu(update, context)


def change_language(update, context):
    user_id = update.message.from_user.id

    buttons = [
        ["🇰🇿 Qaraqalpaq tili", "🇺🇿 O‘zbek tili"],
        ["🇷🇺 Русский язык"]
    ]
    update.message.reply_text(TEXTS["change_lang"][2],  # Standart O‘zbek tili
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))

    # 🚀 Foydalanuvchini ro‘yxatdan o‘tkazmasdan, tilni o‘zgartirish bosqichiga o‘tkazamiz.
    return CHOOSE_LANGUAGE_UPDATE

# ✅ Tilni tanlash
def choose_language(update, context):
    user = update.message.from_user
    lang_choice = update.message.text

    if lang_choice == "🇰🇿 Qaraqalpaq tili":
        lang_id = 1
    elif lang_choice == "🇺🇿 O‘zbek tili":
        lang_id = 2
    elif lang_choice == "🇷🇺 Русский язык":
        lang_id = 3
    else:
        return CHOOSE_LANGUAGE  # Noto‘g‘ri tugma bosilsa, qayta tanlash

    # 📌 Tilni bazada yangilash
    cursor.execute("UPDATE users SET language=? WHERE user_id=?", (lang_id, user.id))
    conn.commit()

    # 🔹 Tanlangan tilni `context.user_data` ichiga saqlaymiz
    context.user_data["language"] = lang_id

    update.message.reply_text(TEXTS["ask_name"][lang_id])
    return ASK_NAME



def send_document(update, context):
    """Hujjat jo‘natish jarayonini boshlash"""
    user_id = update.message.from_user.id

    # 📌 `context.user_data["language"]` mavjudligini tekshiramiz
    if "language" not in context.user_data:
        # 📌 Agar yo‘q bo‘lsa, bazadan olishga harakat qilamiz
        cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            context.user_data["language"] = int(user_data[0])  # Bazadan olinadi
        else:
            context.user_data["language"] = 2  # Agar yo‘q bo‘lsa, standart o‘zbek tili

    lang_id = context.user_data["language"]  # Endi xatolik chiqmaydi

    user_documents[user_id] = {"obektivka": None, "diplom": None, "certifikat": None}

    update.message.reply_text(TEXTS["ask_cv"][lang_id])  # To‘g‘ri tilga mos matn


def handle_document(update, context):
    """Foydalanuvchi hujjat jo‘natganda uni qayta ishlash"""
    user_id = update.message.from_user.id
    # 📌 `context.user_data["language"]` mavjudligini tekshiramiz
    if "language" not in context.user_data:
        # 📌 Agar yo‘q bo‘lsa, bazadan olishga harakat qilamiz
        cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            context.user_data["language"] = int(user_data[0])  # Bazadan olinadi
        else:
            context.user_data["language"] = 2  # Agar yo‘q bo‘lsa, standart o‘zbek tili

    lang_id = context.user_data["language"]  # Endi xatolik chiqmaydi

    if user_id not in user_documents:
        update.message.reply_text("Iltimos, jarayonni boshlash uchun hujjat yuboring")
        return

    document = update.message.document or update.message.photo[-1]  # Rasm yoki fayl qabul qilish

    if user_documents[user_id]["obektivka"] is None:
        user_documents[user_id]["obektivka"] = document
        # update.message.reply_text("✅ Obyektivka qabul qilindi. Endi diplomingizni jo‘nating (PDF, DOC, JPG, ZIP formatlarida).")
        update.message.reply_text(TEXTS["ask_diplom"][lang_id])
    elif user_documents[user_id]["diplom"] is None:
        user_documents[user_id]["diplom"] = document
        keyboard = [
            [InlineKeyboardButton(TEXTS["yes"][lang_id], callback_data="cert_ha")],
            [InlineKeyboardButton(TEXTS["no"][lang_id], callback_data="cert_yoq")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # update.message.reply_text("📜 Sizda chet tili bo‘yicha sertifikat bormi?", reply_markup=reply_markup)
        update.message.reply_text(TEXTS["ask_certificate"][lang_id], reply_markup=reply_markup)
    elif user_documents[user_id]["certifikat"] is None:
        user_documents[user_id]["certifikat"] = document
        # update.message.reply_text("✅ Sertifikat ham qabul qilindi. Hujjatlaringiz jo‘natilmoqda...")
        update.message.reply_text(TEXTS["ask_send"][lang_id])
        send_to_group(update, context, user_id)


def certifikat_callback(update, context):
    """Chet tili sertifikati bor yoki yo‘qligini qayta ishlash"""
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    # 📌 `context.user_data["language"]` mavjudligini tekshiramiz
    if "language" not in context.user_data:
        # 📌 Agar yo‘q bo‘lsa, bazadan olishga harakat qilamiz
        cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            context.user_data["language"] = int(user_data[0])  # Bazadan olinadi
        else:
            context.user_data["language"] = 2  # Agar yo‘q bo‘lsa, standart o‘zbek tili

    lang_id = context.user_data["language"]  # Endi xatolik chiqmaydi


    if query.data == "cert_ha":
        # query.message.reply_text("📜 Iltimos, sertifikatingizni jo‘nating (PDF, DOC, JPG, ZIP formatlarida).")
        query.message.reply_text(TEXTS["ask_cert_upload"][lang_id])
    else:
        # query.message.reply_text("✅ Hujjatlaringiz jo‘natilmoqda...")
        query.message.reply_text(TEXTS["ask_cer_load"][lang_id])
        send_to_group(update, context, user_id)



def send_to_group(update, context, user_id):
    """Guruhga hujjatlarni foydalanuvchi profili bilan birga yuborish"""

    # 📌 `context.user_data["language"]` mavjudligini tekshiramiz
    if "language" not in context.user_data:
        # 📌 Agar yo‘q bo‘lsa, bazadan olishga harakat qilamiz
        cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            context.user_data["language"] = int(user_data[0])  # Bazadan olinadi
        else:
            context.user_data["language"] = 2  # Agar yo‘q bo‘lsa, standart o‘zbek tili

    lang_id = context.user_data["language"]  # Endi xatolik chiqmaydi

    if user_id not in user_documents:
        return

    # 📌 Foydalanuvchi ma'lumotlarini bazadan olish
    cursor.execute("SELECT first_name, last_name, phone FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        first_name, last_name, phone = user_data
    else:
        first_name, last_name, phone = "Noma'lum", "Noma'lum", "Noma'lum"

    # 📌 Profil ma'lumotlarini TEXTS lug‘atidan olib qo‘shish
    caption = (
        f"{TEXTS['send_to_group_doc'][lang_id]}"
        f"{TEXTS['send_to_group_firstname'][lang_id]} {first_name}"
        f"{TEXTS['send_to_group_lastname'][lang_id]} {last_name}"
        f"{TEXTS['send_to_group_phone'][lang_id]} {phone}"
    )

    # 📌 Guruhga foydalanuvchi profil ma'lumotlarini yuborish
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text=caption, parse_mode="Markdown")

    # 📌 Hujjatlarni yuborish
    for key, doc in user_documents[user_id].items():
        if doc:
            if isinstance(doc, Document):  # Agar hujjat bo‘lsa
                context.bot.send_document(chat_id=GROUP_CHAT_ID, document=doc.file_id, caption=f"📄 {key.capitalize()} hujjati")
            else:  # Agar rasm bo‘lsa
                context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=doc.file_id, caption=f"🖼 {key.capitalize()} hujjati")

    # ✅ Foydalanuvchiga hujjatlar jo‘natilganligini bildirish
    update.message.reply_text(TEXTS["completed"][lang_id])

    # 📌 Foydalanuvchi hujjatlarini o‘chirish
    del user_documents[user_id]



def get_chat_id(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Guruh yoki chat ID: `{chat_id}`", parse_mode="Markdown")


# # ❌ Notanish buyruqlarni ushlash
# def unknown(update, context):
#     update.message.reply_text("⚠️ Noto‘g‘ri buyruq! Asosiy menyudan foydalaning.")

# 🏁 Botni ishga tushirish
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher



    # 📌 Bot buyruqlarini o‘rnatish
    set_bot_commands(updater.bot)

    CHOOSE_LANGUAGE, CHOOSE_LANGUAGE_UPDATE, ASK_NAME, ASK_SURNAME, ASK_PHONE, MAIN_MENU = range(6)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_handler)],
        states={
            CHOOSE_LANGUAGE: [MessageHandler(Filters.text, choose_language)],
            CHOOSE_LANGUAGE_UPDATE: [MessageHandler(Filters.text, choose_language)],  # 🔹 Tilni o‘zgartirish uchun
            ASK_NAME: [MessageHandler(Filters.text, get_name)],
            ASK_SURNAME: [MessageHandler(Filters.text, get_surname)],
            ASK_PHONE: [MessageHandler(Filters.contact | Filters.text, get_phone)],
            MAIN_MENU: [
                MessageHandler(
                    Filters.regex(TEXTS["profile_btn"][1]) |
                    Filters.regex(TEXTS["profile_btn"][2]) |
                    Filters.regex(TEXTS["profile_btn"][3]), show_profile),
                MessageHandler(
                    Filters.regex(TEXTS["jobs_btn"][1]) |
                    Filters.regex(TEXTS["jobs_btn"][2]) |
                    Filters.regex(TEXTS["jobs_btn"][3]), send_document),
                MessageHandler(
                    Filters.regex(TEXTS["change_lang"][1]) |
                    Filters.regex(TEXTS["change_lang"][2]) |
                    Filters.regex(TEXTS["change_lang"][3]), change_language)
            ],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(MessageHandler(Filters.document | Filters.photo, handle_document))
    dispatcher.add_handler(CallbackQueryHandler(certifikat_callback, pattern="^cert_"))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("getid", get_chat_id))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
