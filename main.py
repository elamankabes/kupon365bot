import telebot
import json
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7820035162:AAEGsSfAZW1Ql873ABZW69GtiFnrqKIDcH4"
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
        text = (
            f"🛍 {coupon['title']}\n"
            f"💬 Промокод: `{coupon['code']}`\n"
            f"📅 До: {coupon['end_date']}\n"
            f"🎁 {coupon['discount']}\n\n"
            f"⚠️ Промокод работает только по кнопке ниже!"
        )

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Перейти на сайт 🔗", url=coupon['link']))

        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "К сожалению, сейчас нет доступных купонов 😢")

bot.polling()
