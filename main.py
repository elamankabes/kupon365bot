import telebot
import json
import random
from telebot import types
import os

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /coupon, чтобы получить свежий купон 🎁")

@bot.message_handler(commands=['coupon'])
def send_coupon(message):
    try:
        with open("coupons.json", "r", encoding="utf-8") as f:
            coupons = json.load(f)
    except:
        coupons = []

    if coupons:
        coupon = random.choice(coupons)

        # Текст купона
        text = (
            f"🛍 {coupon['shop']} — {coupon['title']}\n"
            f"💬 Промокод: `{coupon['code']}`\n"
            f"📅 До: {coupon['end_date']}\n"
            f"🎁 {coupon['discount']}\n\n"
            f"⚠️ Любой промокод или купон работает только по своей ссылке!"
        )

        # Кнопка перехода
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🔗 Перейти на сайт", url=coupon['link'])
        markup.add(btn)

        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "К сожалению, сейчас нет доступных купонов 😢")

bot.polling()
