import telebot
from telebot import types

# 1. Bot tokeningiz va admin ID raqamingiz
TOKEN = "9194978768:AAGXaqSU9j5ZpFEJXZ4hM7dXjs3zqkqFqaU"
ADMIN_ID = 304538764  # O'z Telegram ID raqamingizni yozing

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# 2. 6 ta shartning to'g'ri javob kodlari (bularni o'zingiz xohlagancha o'zgartirishingiz mumkin)
SHART_KODLARI = {
    1: "KOD111",
    2: "KOD222",
    3: "KOD333",
    4: "KOD444",
    5: "KOD555",
    6: "KOD666"
}

# 3. Jamoalar va ularning har xil (aralash) tartibdagi shartlar marshruti
JAMOALAR = {
    "Gryffindor": {
        "marshrut": [2, 5, 1, 4, 3, 6],
        "joriy_qadam": 0
    },
    "Varislar": {
        "marshrut": [4, 1, 3, 6, 2, 5],
        "joriy_qadam": 0
    },
    "Zakovat": {
        "marshrut": [1, 3, 5, 2, 4, 6],
        "joriy_qadam": 0
    }
}

# Foydalanuvchi qaysi jamoaga tegishli ekanligini saqlash
user_jamoasi = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for jamoa in JAMOALAR.keys():
        markup.add(types.KeyboardButton(jamoa))
    
    bot.send_message(
        message.chat.id,
        "🎯 *WikiKlub Kvest O'yiniga xush kelibsiz!*\n\n"
        "Iltimos, pastdagi tugmalardan o'z jamoangizni tanlang:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in JAMOALAR.keys())
def select_team(message):
    jamoa = message.text
    user_id = message.from_user.id
    user_jamoasi[user_id] = jamoa
    
    qadam = JAMOALAR[jamoa]["joriy_qadam"]
    shart_raqami = JAMOALAR[jamoa]["marshrut"][qadam]
    
    bot.send_message(
        message.chat.id,
        f"✅ Siz *{jamoa}* jamoasi sifatida muvaffaqiyatli ro'yxatdan o'tdingiz!\n\n"
        f"📌 Sizning **1-vazifangiz**: Qo'lingizdagi qog'ozdagi *{shart_raqami}-shartni* bajaring va chiqqan kodni shu botga yuboring.",
        reply_markup=types.ReplyKeyboardRemove()
    )

@bot.message_handler(func=lambda message: message.from_user.id in user_jamoasi)
def handle_code_submission(message):
    user_id = message.from_user.id
    jamoa = user_jamoasi[user_id]
    kiritilgan_kod = message.text.strip()
    
    qadam = JAMOALAR[jamoa]["joriy_qadam"]
    marshrut = JAMOALAR[jamoa]["marshrut"]
    
    # Agar jamoa barcha bosqichlarni tugatgan bo'lsa
    if qadam >= len(marshrut):
        bot.send_message(
            message.chat.id, 
            "🎉 Siz allaqachon barcha shartlarni bajarib bo'lgansiz!"
        )
        return
        
    joriy_shart_raqami = marshrut[qadam]
    togri_kod = SHART_KODLARI[joriy_shart_raqami]
    
    # Kodni solishtirish
    if kiritilgan_kod == togri_kod:
        # Keyingi qadamga o'tkazamiz
        JAMOALAR[jamoa]["joriy_qadam"] += 1
        yangi_qadam = JAMOALAR[jamoa]["joriy_qadam"]
        
        bot.send_message(
            message.chat.id,
            "🎉 *Tabriklayman! Kod to'g'ri.*\n\n"
            "Joyingizdagi tashkilotchiga yaqinlashib, keyingi shart qog'ozini oling! 📄"
        )
        
        # Adminga xabar yuborish
        if yangi_qadam < len(marshrut):
            keyingi_shart = marshrut[yangi_qadam]
            admin_xabar = (
                f"📍 *{jamoa}* jamoasi {joriy_shart_raqami}-shart kodini to'g'ri topdi!\n"
                f"Ularga *{keyingi_shart}-shart* qog'ozini berishingiz mumkin."
            )
        else:
            admin_xabar = f"🏆 *{jamoa}* jamoasi **BARCHA** shartlarni bajarib kvestni muvaffaqiyatli yakunladi!"
            
        bot.send_message(ADMIN_ID, admin_xabar)
        
    else:
        bot.send_message(
            message.chat.id,
            "❌ *Kod xato!* Qaytadan tekshirib, to'g'ri kodni yuboring."
        )

# Botni ishga tushirish
if __name__ == "__main__":
    print("Kvest bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling(skip_pending=True)