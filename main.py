import telebot
import requests
import time
import threading

# Токен вашего бота, который вы скинули
BOT_TOKEN = "8645065740:AAE3dxaWdtLcQdRAg0n247o583uHJ1SfoOI"

# Ваш личный Telegram ID, который вы скинули
MY_TELEGRAM_ID = 7674113183

# Границы цен для уведомлений (можете изменить под себя)
ALERT_LOW = 0.05
ALERT_HIGH = 1.50

bot = telebot.TeleBot(BOT_TOKEN)

def get_prl_price():
    # Получение цены пары PRL/USDT с биржи SafeTrade
    url = "https://safe.trade"
    try:
        response = requests.get(url).json()
        return float(response['ticker']['last'])
    except Exception:
        return None

def price_tracker():
    """Фоновый трекер: проверяет цену каждые 5 минут и шлет уведомления"""
    while True:
        price = get_prl_price()
        if price:
            if price <= ALERT_LOW:
                bot.send_message(MY_TELEGRAM_ID, f"⚠️ Цена PRL упала: ${price:.4f} USDT")
            elif price >= ALERT_HIGH:
                bot.send_message(MY_TELEGRAM_ID, f"🚀 Цена PRL выросла: ${price:.4f} USDT")
        time.sleep(300)  # Пауза 5 минут

@bot.message_handler(commands=['start', 'prl'])
def send_price(message):
    """Ответ на ручные команды пользователя в чате бота"""
    price = get_prl_price()
    if price:
        bot.reply_to(message, f"🟢 Курс Pearl (PRL): ${price:.4f} USDT на SafeTrade")
    else:
        bot.reply_to(message, "❌ Ошибка сети SafeTrade. Попробуйте позже.")

if __name__ == "__main__":
    # Запуск фонового мониторинга цен
    threading.Thread(target=price_tracker, daemon=True).start()
    # Запуск самого бота
    bot.infinity_polling()
