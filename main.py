import telebot
import json
import random

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
        text = f"🛍 {coupon['title']}\n💬 Промокод: `{coupon['code']}`\n📅 До: {coupon['end_date']}\n🎁 {coupon['discount']}\n🔗 [Перейти по ссылке]({coupon['link']})\n⚠️ Любой промокод работает только по своей ссылке!"
        bot.send_message(message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "К сожалению, сейчас нет доступных купонов 😢")

bot.polling()
