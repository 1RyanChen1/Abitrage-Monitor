import requests
import time

# Telegram Bot ID/ User name Input
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# Support Coin）
symbols = ["BTC", "ETH", "SOL"]

# Binance price
def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url).json()
        return float(data['price'])
    except:
        print(f"Error fetching Binance price for {symbol}")
        return None

# Coinbase Price
def get_coinbase_price(symbol):
    try:
        url = f"https://api.exchange.coinbase.com/products/{symbol}-USD/ticker"
        data = requests.get(url).json()
        return float(data['price'])
    except:
        print(f"Error fetching Coinbase price for {symbol}")
        return None

#Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Error sending message to Telegram")
    except Exception as e:
        print(f"Error: {e}")

# Checking Arbitrage
def check_pair(symbol, threshold=1.0):
    binance = get_binance_price(symbol)
    coinbase = get_coinbase_price(symbol)

    if binance is None or coinbase is None:
        return

    diff = abs(binance - coinbase)
    print(f"{symbol}: Binance = {binance:.2f}, Coinbase = {coinbase:.2f} | Δ = {diff:.2f}")

    if coinbase - binance > threshold:
        message = f">>> Arbitrage Opportunity: BUY on Binance, SELL on Coinbase | Profit ≈ {coinbase - binance:.2f} USD for {symbol}"
        send_telegram_message(message)
    elif binance - coinbase > threshold:
        message = f">>> Arbitrage Opportunity: BUY on Coinbase, SELL on Binance | Profit ≈ {binance - coinbase:.2f} USD for {symbol}"
        send_telegram_message(message)
    else:
        print("No significant arbitrage.\n")

# Main loop
def run_monitor(threshold=1.0, interval=10):
    while True:
        print("=" * 60)
        for symbol in symbols:
            check_pair(symbol, threshold)
        time.sleep(interval)

if __name__ == "__main__":
    run_monitor(threshold=1.5, interval=10)  