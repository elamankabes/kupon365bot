import telebot
import json
import random
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import schedule
import time
import threading

TOKEN = "ВАШ_ТОКЕН_ОТСЮДА_ИЗ_РЕНДЕРА"

bot = telebot.TeleBot(TOKEN)

XML_URL = "https://export.admitad.com/kz/webmaster/websites/2830156/coupons/export/?website=2830156&region=00&language=&only_my=on&keyword=&code=nuajwzcdqc&user=Elamankabew&format=xml&v=1"

def fetch_coupons():
    response = requests.get(XML_URL)
    tree = ET.fromstring(response.content)
    coupons = []

    for item in tree.findall(".//coupon"):
        title = item.findtext("campaign_name", "Без названия")
        code = item.findtext("code", "Нет кода")
        end_date = item.findtext("date_end", "")
        discount = item.findtext("discount", "Без описания")
        link = item.findtext("goto_link", "#")

        try:
            date_end = datetime.strptime(end_date, "%Y-%m-%d")
            if date_end >= datetime.now():
                coupons.append({
                    "title": title,
                    "code": code,
                    "discount": discount,
                    "link": link,
                    "end_date": end_date
                })
        except:
            continue

    with open("coupons.json", "w", encoding="utf-8") as f:
        json.dump(coupons, f, ensure_ascii=False, indent=2)

def schedule_fetch():
    schedule.every(6).hours.do(fetch_coupons)
    while True:
        schedule.run_pending()
        time.sleep(10)

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
            f"🎁 {coupon['discount']}\n"
            f"🔗 [Перейти по ссылке]({coupon['link']})\n\n"
            f"⚠️ Любой промокод работает только по своей ссылке!"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "К сожалению, сейчас нет доступных купонов 😢")

# Запускаем парсер в отдельном потоке
threading.Thread(target=schedule_fetch).start()

# Запускаем бота
bot.polling()
