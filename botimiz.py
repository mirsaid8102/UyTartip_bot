
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

# Sizning Tokeningiz
API_TOKEN = '8296108535:AAFSdXlDY2wcYfM51tRhUHD4AE4KPXUeHjg'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- MA'LUMOTLAR ---
bolalar = ["Shaxri", "Beglan", "Mirsaid", "Dilshodbek", "Sultan", "Muratbek (Oshpaz)"]

navbatchilar = {
    1: "Shaxri", 2: "Beglan", 3: "Mirsaid", 
    4: "Dilshodbek", 5: "Sultan", 6: "Dam olish", 7: "Dam olish"
}

ovqatlar = {
    1: "Makaron", 2: "Palaw", 3: "Shorpa", 
    4: "Greshka", 5: "Nan quwirdaq", 6: "Erkin menu", 7: "Erkin menu"
}

# --- TUGMALAR ---
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("📋 Bugun kim navbatchi?", "🍲 Haftalik Menu")
main_menu.add("⭐ Bollarni baholash", "💰 Kvartira Bank")
main_menu.add("📍 Uy lokatsiyasi")

# --- FUNKSIYALAR ---

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum @UyTartib_bot ga xush kelibsiz!\n\n"
        "Bu yerda hamma bir-biriga ball qo'yishi va tartibni ko'rishi mumkin.",
        reply_markup=main_menu
    )

@dp.message_handler(lambda m: m.text == "📋 Bugun kim navbatchi?")
async def get_navbatchi(message: types.Message):
    kun = datetime.now().isoweekday()
    ism = navbatchilar.get(kun, "Noma'lum")
    await message.answer(f"📅 Bugungi navbatchi: {ism}")

@dp.message_handler(lambda m: m.text == "🍲 Haftalik Menu")
async def get_menu(message: types.Message):
    text = "🍴 Haftalik Menu:\n"
    for k, v in ovqatlar.items():
        kun = ["Dush", "Sesh", "Chor", "Pay", "Juma", "Shan", "Yak"][k-1]
        text += f"🔹 {kun}: {v}\n"
    await message.answer(text)

@dp.message_handler(lambda m: m.text == "⭐ Bollarni baholash")
async def rate_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for bola in bolalar:
        kb.insert(KeyboardButton(f"Baholash: {bola}"))
    kb.add("⬅️ Orqaga")
    await message.answer("Kimga ball qo'ymoqchisiz?", reply_markup=kb)

@dp.message_handler(lambda m: m.text.startswith("Baholash: "))
async def choose_score(message: types.Message):
    kim = message.text.replace("Baholash: ", "")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("1", "2", "3", "4", "5").add("⬅️ Orqaga")
    await message.answer(f"{kim} uchun necha ball berasiz?", reply_markup=kb)

@dp.message_handler(lambda m: m.text in ["1", "2", "3", "4", "5"])
async def save_score(message: types.Message):
    await message.answer(f"Rahmat! Bahoyingiz qabul qilindi ✅", reply_markup=main_menu)

@dp.message_handler(lambda m: m.text == "💰 Kvartira Bank")
async def bank_info(message: types.Message):
    text = (
        "🏦 Kvartira Banki\n"
        "💰 Balans: 0 so'm\n"
        "❌ Pul solmaganlar: Hamma\n\n"
        "Pul solgan bo'lsangiz, 'Pul qo'shdim' deb yozing."
    )
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add("💵 Pul qo'shdim", "⬅️ Orqaga")
    await message.answer(text, reply_markup=kb)

@dp.message_handler(lambda m: m.text == "📍 Uy lokatsiyasi")
async def send_loc(message: types.Message):
    await bot.send_location(message.chat.id, 42.4601, 59.6120)
    await message.answer("Uyimiz lokatsiyasi 📍")

@dp.message_handler(lambda m: m.text == "⬅️ Orqaga")
async def back(message: types.Message):
    await message.answer("Asosiy menyu", reply_markup=main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)