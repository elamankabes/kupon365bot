import os
import telebot
import json
import random

# Получаем токен из переменной окружения
TOKEN = os.environ.get("BOT_TOKEN")

# Проверка на случай, если токен не передан
if not TOKEN or ":" not in TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не установлена или имеет неверный формат!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /coupon, чтобы получить свежий купон 🎁")

@bot.message_handler(commands=['coupon'])
def send_coupon(message):
    try:
        with open("coupons.json", "r", encoding="utf-8") as f:
            coupons = json.load(f)
    except Exception as e:
        coupons = []
        print(f"Ошибка при чтении coupons.json: {e}")

    if coupons:
        coupon = random.choice(coupons)
        text = (
            f"🛍 {coupon['title']}\n"
            f"💬 Промокод: `{coupon['code']}`\n"
            f"📅 До: {coupon['end_date']}\n"
            f"🎁 {coupon['discount']}\n"
            f"🔗 [Перейти по ссылке]({coupon['link']})"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "К сожалению, сейчас нет доступных купонов 😢")

bot.polling(non_stop=True)
