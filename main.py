import telebot
import json
import random
import schedule
import time
import threading
from parser import fetch_coupons  # импортируем функцию из parser.py

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

# Запускаем автообновление купонов по расписанию
def run_scheduler():
    schedule.every(6).hours.do(fetch_coupons)  # обновлять каждые 6 часов
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск планировщика в отдельном потоке
threading.Thread(target=run_scheduler, daemon=True).start()

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
