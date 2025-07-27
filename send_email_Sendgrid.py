import time
import os
from dotenv import load_dotenv
from datetime import datetime
from requests import get
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv(dotenv_path="./sendgrid.env") # Load Environment Variables

def sendEmail(message,status=1):
    for receiver_email in receiver_emails:
        try:
            msg = Mail(from_email=sender_email,
                       to_emails=receiver_email,
                       subject=f"📅 Daily Crypto Report - {datetime.today().date().strftime('%B %d, %Y')}",
                       html_content=message)

            sg = SendGridAPIClient(api_key=SEND_GRID_API)
            response = sg.send(msg)
            if response.status_code == 202:
                print("Email Sent Successfully!")
            else:
                print("Email could not be send!")

        except Exception as e:
            print(f"Email could not be send!: {e}")


sender_email = os.getenv("SENDER_EMAIL")
receiver_emails = os.getenv("RECEIVER_EMAILS").split(",")
SEND_GRID_API = os.getenv("SEND_GRID_API")

BTC_PURCHASE_PRICE = float(os.getenv("BTC_PURCHASE_PRICE"))
ETH_PURCHASE_PRICE = float(os.getenv("ETH_PURCHASE_PRICE"))
LTC_PURCHASE_PRICE = float(os.getenv("LTC_PURCHASE_PRICE"))
SOL_PURCHASE_PRICE = float(os.getenv("SOL_PURCHASE_PRICE"))
USD_PURCHASED_PRICE = float(os.getenv("USD_PURCHASED_PRICE"))

BTC_INVESTED = float(os.getenv("BTC_INVESTED"))
ETH_INVESTED = float(os.getenv("ETH_INVESTED"))
SOL_INVESTED = float(os.getenv("SOL_INVESTED"))
LTC_INVESTED = float(os.getenv("LTC_INVESTED"))

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# ------------------------------
# Fetch Live Data
# ------------------------------
gotData = True
for _ in range(5):
    pkr_request = get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD")
    coin_request = get(url="https://api.coingecko.com/api/v3/simple/price",
                       params={"ids": "bitcoin,ethereum,solana,litecoin","vs_currencies": "usd"},
                       headers={'Accept': 'application/json','x-cg-demo-api-key': os.getenv('COIN_GECKO_API')}
                       )
    if pkr_request.status_code != 200 or coin_request.status_code != 200:
        gotData = False
        time.sleep(30)
    else:
        pkr_rate = pkr_request.json()['conversion_rates']['PKR']
        coins = coin_request.json()
        break


if gotData:
    btc_price = coins['bitcoin']['usd']
    eth_price = coins['ethereum']['usd']
    sol_price = coins['solana']['usd']
    ltc_price = coins['litecoin']['usd']

    btc_amount = BTC_INVESTED / BTC_PURCHASE_PRICE
    eth_amount = ETH_INVESTED / ETH_PURCHASE_PRICE
    sol_amount = SOL_INVESTED / SOL_PURCHASE_PRICE
    ltc_amount = LTC_INVESTED / LTC_PURCHASE_PRICE

    btc_now = btc_price * btc_amount
    eth_now = eth_price * eth_amount
    sol_now = sol_price * sol_amount
    ltc_now = ltc_price * ltc_amount

    btc_profit = btc_now - BTC_INVESTED
    eth_profit = eth_now - ETH_INVESTED
    sol_profit = sol_now - SOL_INVESTED
    ltc_profit = ltc_now - LTC_INVESTED

    btc_percent = (btc_profit / BTC_INVESTED) * 100
    eth_percent = (eth_profit / ETH_INVESTED) * 100
    sol_percent = (sol_profit / SOL_INVESTED) * 100
    ltc_percent = (ltc_profit / LTC_INVESTED) * 100

    total_now_usd = btc_now + eth_now + sol_now + ltc_now
    total_invested_usd = BTC_INVESTED + ETH_INVESTED + SOL_INVESTED + LTC_INVESTED
    total_profit = total_now_usd - total_invested_usd
    total_percent = (total_profit / total_invested_usd) * 100
    final_amount_pkr = total_now_usd * pkr_rate * 0.98

    # Read HTML template
    with open("crypto_report.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Replace placeholders in HTML
    replacements = {
        "{ pkr_rate }": f"{pkr_rate:.2f}",
        "{ usd_purchased_price }": f"{USD_PURCHASED_PRICE}",
        "{ total_invested_usd }": f"{total_invested_usd:.2f}",
        "{ total_invested_pkr }": f"{total_invested_usd * USD_PURCHASED_PRICE:,.0f}",
        "{ total_now_usd }": f"{total_now_usd:.2f}",
        "{ total_profit }": f"{total_profit:+.2f}",
        "{ total_percent }": f"{total_percent:+.2f}",
        "{ final_amount_pkr }": f"{final_amount_pkr:,.0f}",

        "{ eth_invested }": f"{ETH_INVESTED}",
        "{ eth_purchase_price }": f"{ETH_PURCHASE_PRICE}",
        "{ eth_amount }": f"{eth_amount:.5f}",
        "{ eth_price }": f"{eth_price:.2f}",
        "{ eth_now }": f"{eth_now:.2f}",
        "{ eth_profit }": f"{eth_profit:+.2f}",
        "{ eth_percent }": f"{eth_percent:+.2f}",

        "{ btc_invested }": f"{BTC_INVESTED}",
        "{ btc_purchase_price }": f"{BTC_PURCHASE_PRICE}",
        "{ btc_amount }": f"{btc_amount:.6f}",
        "{ btc_price }": f"{btc_price:.2f}",
        "{ btc_now }": f"{btc_now:.2f}",
        "{ btc_profit }": f"{btc_profit:+.2f}",
        "{ btc_percent }": f"{btc_percent:+.2f}",

        "{ sol_invested }": f"{SOL_INVESTED}",
        "{ sol_purchase_price }": f"{SOL_PURCHASE_PRICE}",
        "{ sol_amount }": f"{sol_amount:.4f}",
        "{ sol_price }": f"{sol_price:.2f}",
        "{ sol_now }": f"{sol_now:.2f}",
        "{ sol_profit }": f"{sol_profit:+.2f}",
        "{ sol_percent }": f"{sol_percent:+.2f}",

        "{ ltc_invested }": f"{LTC_INVESTED}",
        "{ ltc_purchase_price }": f"{LTC_PURCHASE_PRICE}",
        "{ ltc_amount }": f"{ltc_amount:.4f}",
        "{ ltc_price }": f"{ltc_price:.2f}",
        "{ ltc_now }": f"{ltc_now:.2f}",
        "{ ltc_profit }": f"{ltc_profit:+.2f}",
        "{ ltc_percent }": f"{ltc_percent:+.2f}",

        "{ NOW_TIME }": datetime.now().strftime('%I:%M %p')
    }

    for key, val in replacements.items():
        html_template = html_template.replace(key, val)

    # Send HTML
    sendEmail(html_template)

else:
    sendEmail("<h2>❌ API failed after retries. Check your internet or keys.</h2>")