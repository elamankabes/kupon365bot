import telebot
import json
import random
from telebot import types

TOKEN = "7820035162:AAEGsSfAZW1Ql873ABZW69GtiFnrqKIDcH4"
bot = telebot.TeleBot(TOKEN)

# Загружаем купоны из JSON
def load_coupons():
    try:
        with open("coupons.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    coupons = load_coupons()
    if not coupons:
        bot.send_message(message.chat.id, "К сожалению, купоны временно недоступны 😢")
        return

    # Получаем уникальные названия магазинов
    stores = list(set([c["title"] for c in coupons if "title" in c]))
    stores.sort()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(title) for title in stores]
    markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Привет! 👋 Выберите магазин, чтобы получить доступные купоны:",
        reply_markup=markup
    )

# Обработка выбора магазина
@bot.message_handler(func=lambda message: True)
def send_store_coupons(message):
    coupons = load_coupons()
    store_coupons = [c for c in coupons if c.get("title") == message.text]

    if not store_coupons:
        bot.send_message(message.chat.id, "Купоны для этого магазина пока недоступны 😢")
        return

    for coupon in store_coupons[:5]:  # Покажем до 5 купонов
        text = (
            f"🛍 {coupon['title']}\n"
            f"💬 Промокод: `{coupon['code']}`\n"
            f"📅 До: {coupon['end_date']}\n"
            f"🎁 {coupon['discount']}\n\n"
            f"⚠️ *Промокод работает только по кнопке ниже!*"
        )

        btn = types.InlineKeyboardMarkup()
        btn.add(types.InlineKeyboardButton("👉 Перейти на сайт", url=coupon['link']))

        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=btn)

bot.polling()
