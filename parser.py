import requests
import xml.etree.ElementTree as ET
import json

# 🔗 Укажи здесь свою ссылку на XML с промокодами
XML_URL = "https://твой-ссылка-на-фид.xml"

def fetch_coupons():
    response = requests.get(XML_URL)
    root = ET.fromstring(response.content)

    coupons = []
    for offer in root.findall("offer"):
        title = offer.findtext("name")
        code = offer.findtext("coupon_code")
        link = offer.findtext("url")
        end_date = offer.findtext("date_end")
        discount = offer.findtext("discount")

        if not all([title, code, link]):
            continue

        coupons.append({
            "title": title.strip(),
            "code": code.strip(),
            "link": link.strip(),
            "end_date": end_date.strip() if end_date else "Не указано",
            "discount": discount.strip() if discount else "Скидка по купону",
            "note": "Промокод работает только по своей ссылке 🔒"
        })

    with open("coupons.json", "w", encoding="utf-8") as f:
        json.dump(coupons, f, ensure_ascii=False, indent=2)

    print(f"✅ Загружено и сохранено {len(coupons)} купонов в coupons.json")

if __name__ == "__main__":
    fetch_coupons()
