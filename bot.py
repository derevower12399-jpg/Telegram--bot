import logging
import os
import telebot
from telebot import types

logging.basicConfig(level=logging.INFO)

# --- TOKEN з Railway Variables ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

CONTACT = "@Viopt35"
ADMIN_ID = 8647714388


# --- MENUS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("🟣🛒 Замовити"),
        types.KeyboardButton("🟣💰 Прайс"),
        types.KeyboardButton("🟣📞 Зв'язок")
    )
    return markup


def order_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("🎨 Аватарка"),
        types.KeyboardButton("🎬 Анімація")
    )
    markup.row(
        types.KeyboardButton("📸 Оживити фото")
    )
    markup.row(
        types.KeyboardButton("🧩 Стікери 5 шт"),
        types.KeyboardButton("🧩 Стікери 10 шт")
    )
    markup.row(types.KeyboardButton("⬅️ Назад"))
    return markup


def pay_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("💳 Я оплатив"),
        types.KeyboardButton("⬅️ Назад")
    )
    return markup


# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🟣 Привіт! Обери дію:",
        reply_markup=main_menu()
    )


# --- ORDER ---
@bot.message_handler(func=lambda m: m.text == "🟣🛒 Замовити")
def order(message):
    bot.send_message(message.chat.id, "Що хочеш замовити? ✨", reply_markup=order_menu())


# --- SERVICES ---
@bot.message_handler(func=lambda m: m.text in [
    "🎨 Аватарка",
    "🎬 Анімація",
    "📸 Оживити фото",
    "🧩 Стікери 5 шт",
    "🧩 Стікери 10 шт"
])
def choose_service(message):
    bot.send_message(
        message.chat.id,
        f"✨ Ти обрав: {message.text}\n\n💳 Оплата: {CONTACT}\n\nПісля оплати натисни 👇",
        reply_markup=pay_menu()
    )


# --- PRICE ---
@bot.message_handler(func=lambda m: m.text == "🟣💰 Прайс")
def price(message):
    bot.send_message(
        message.chat.id,
        "💰 Прайс:\n\n"
        "🎨 Аватарка — 50 грн\n"
        "🎬 Анімація — 90 грн\n"
        "📸 Оживити фото — 70 грн\n\n"
        "🧩 Стікери:\n"
        "5 шт — 55 грн\n"
        "10 шт — 75 грн"
    )


# --- CONTACT ---
@bot.message_handler(func=lambda m: m.text == "🟣📞 Зв'язок")
def contact(message):
    bot.send_message(message.chat.id, f"📞 {CONTACT}")


# --- PAID ---
@bot.message_handler(func=lambda m: m.text == "💳 Я оплатив")
def paid(message):
    username = message.from_user.username or "no_username"

    bot.send_message(
        ADMIN_ID,
        f"💰 НОВА ОПЛАТА!\nUser: @{username}\nID: {message.from_user.id}"
    )

    bot.send_message(
        message.chat.id,
        "✅ Дякую за оплату! Я зв'яжусь з вами 🤝",
        reply_markup=main_menu()
    )


# --- BACK ---
@bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
def back(message):
    bot.send_message(message.chat.id, "Головне меню 🟣", reply_markup=main_menu())


# --- FALLBACK ---
@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(message.chat.id, "⚠️ Використай кнопки 👇", reply_markup=main_menu())


# --- START BOT ---
print("Bot is running...")
bot.infinity_polling(skip_pending=True)
