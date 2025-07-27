import time
import smtplib
from datetime import datetime
from requests import get
from dotenv import load_dotenv
import os

# ============================
# 📦 Load Environment Variables
# ============================
load_dotenv(dotenv_path="smpt_variables.env")

# ============================
# 📧 Send Email Function
# ============================
def sendEmail(msg, status=1):
    sender_email = os.getenv('EMAIL_USER')
    sender_email_key_pass = os.getenv('EMAIL_PASS')

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=sender_email, password=sender_email_key_pass)

        if status:
            # Send to recipients
            recipients = os.getenv('RECIPIENTS_EMAILS').split(',')
            for receiver in recipients:
                try:
                    connection.sendmail(
                        from_addr=sender_email,
                        to_addrs=receiver,
                        msg=msg.encode('utf-8')
                    )
                    print("Email Sent Successfully!")
                except:
                    pass
        else:
            # Send error to admin only
            admin_email = os.getenv('ADMIN_EMAIL')
            connection.sendmail(
                from_addr=sender_email,
                to_addrs=admin_email,
                msg=msg.encode('utf-8')
            )

# ============================
# 🌐 API Request Configuration
# ============================
coins_request_data = {
    "ids": os.getenv('MY_COINS'),
    "vs_currencies": os.getenv('CURRENCIES')
}

# ============================
# 📊 Load Investment Data
# ============================
# Purchase Prices
btc_purchase_price = float(os.getenv("BTC_PURCHASE_PRICE"))
eth_purchase_price = float(os.getenv("ETH_PURCHASE_PRICE"))
ltc_purchase_price = float(os.getenv("LTC_PURCHASE_PRICE"))
sol_purchase_price = float(os.getenv("SOL_PURCHASE_PRICE"))
usd_purchased_price = float(os.getenv("USD_PURCHASED_PRICE"))

# Investment Amounts
btc_invested = float(os.getenv("BTC_INVESTED"))
eth_invested = float(os.getenv("ETH_INVESTED"))
sol_invested = float(os.getenv("SOL_INVESTED"))
ltc_invested = float(os.getenv("LTC_INVESTED"))

# ============================
# 🔁 Get Live Data Loop
# ============================
gotData = True
for _ in range(5):
    # Get USD to PKR rate
    pkr_request = get(f"https://v6.exchangerate-api.com/v6/{os.getenv('EXCHANGE_API_KEY')}/latest/USD")

    # Get live coin prices
    coin_request = get("https://api.coingecko.com/api/v3/simple/price", params=coins_request_data)

    # Retry if failed
    if pkr_request.status_code != 200 or coin_request.status_code != 200:
        gotData = False
        time.sleep(30)
    else:
        pkr_rate = pkr_request.json()['conversion_rates']['PKR']
        coins = coin_request.json()
        break

# ============================
# 🧾 Calculate and Send Report
# ============================
if gotData:
    # Current Prices
    btc_price = coins['bitcoin']['usd']
    eth_price = coins['ethereum']['usd']
    sol_price = coins['solana']['usd']
    ltc_price = coins['litecoin']['usd']

    # Amounts Bought
    btc_amount = btc_invested / btc_purchase_price
    eth_amount = eth_invested / eth_purchase_price
    sol_amount = sol_invested / sol_purchase_price
    ltc_amount = ltc_invested / ltc_purchase_price

    # Current Values
    btc_now = btc_price * btc_amount
    eth_now = eth_price * eth_amount
    sol_now = sol_price * sol_amount
    ltc_now = ltc_price * ltc_amount

    # Profit/Loss
    btc_profit = btc_now - btc_invested
    eth_profit = eth_now - eth_invested
    sol_profit = sol_now - sol_invested
    ltc_profit = ltc_now - ltc_invested

    btc_percent = (btc_profit / btc_invested) * 100
    eth_percent = (eth_profit / eth_invested) * 100
    sol_percent = (sol_profit / sol_invested) * 100
    ltc_percent = (ltc_profit / ltc_invested) * 100

    # Total Summary
    total_now_usd = btc_now + eth_now + sol_now + ltc_now
    total_invested_usd = btc_invested + eth_invested + sol_invested + ltc_invested
    total_profit = total_now_usd - total_invested_usd
    total_percent = (total_profit / total_invested_usd) * 100
    final_amount_pkr = total_now_usd * pkr_rate * 0.98  # After 2% fee

    # Email Body
    crypto_msg = (
        f"Subject: 📅 Daily Crypto Report - {datetime.today().date().strftime('%B %d, %Y')}\n\n"
        f"💱 USD to PKR Current Rate: {pkr_rate:.2f}\n"
        f"💼 Total Invested: ${total_invested_usd:.2f} at rate Rs. {usd_purchased_price} -> (Rs. {total_invested_usd * usd_purchased_price})\n"
        f"💰 Current Value: ${total_now_usd:.2f}\n"
        f"📈 Net Profit/Loss: ${total_profit:.2f} ({total_percent:+.2f}%)\n"
        f"🏦 Estimated PKR (after 2% fee)*: Rs. {final_amount_pkr:,.0f}\n"
        f"───────────────────────────────\n\n"

        f"🪙 Ethereum (ETH)\n"
        f"• Bought: ${eth_invested} @ ${eth_purchase_price} --> {eth_amount:.5f} ETH\n"
        f"• Now: ${eth_price:.2f} → ${eth_now:.2f}\n"
        f"• Profit/Loss: ${eth_profit:+.2f} ({eth_percent:+.2f}%)\n\n"

        f"🪙 Bitcoin (BTC)\n"
        f"• Bought: ${btc_invested} @ ${btc_purchase_price} --> {btc_amount:.6f} BTC\n"
        f"• Now: ${btc_price:.2f} --> ${btc_now:.2f}\n"
        f"• Profit/Loss: ${btc_profit:+.2f} ({btc_percent:+.2f}%)\n\n"

        f"🪙 Solana (SOL)\n"
        f"• Bought: ${sol_invested} @ ${sol_purchase_price} --> {sol_amount:.4f} SOL\n"
        f"• Now: ${sol_price:.2f} --> ${sol_now:.2f}\n"
        f"• Profit/Loss: ${sol_profit:+.2f} ({sol_percent:+.2f}%)\n\n"

        f"🪙 Litecoin (LTC)\n"
        f"• Bought: ${ltc_invested} @ ${ltc_purchase_price} --> {ltc_amount:.4f} LTC\n"
        f"• Now: ${ltc_price:.2f} --> ${ltc_now:.2f}\n"
        f"• Profit/Loss: ${ltc_profit:+.2f} ({ltc_percent:+.2f}%)\n\n"

        f"───────────────────────────────\n\n"
        f"🧠 Report Generated By: Muhammad Ali's Auto Crypto Tracker 📊\n\n"

        f"🕒 Auto-tracked via PythonAnywhere at Pakistani Standard Time (PKT): {datetime.now().strftime('%I:%M %p')}\n\n"

        f"📉 This update is calculated using real-time data from CoinGecko and USD/PKR rates from Exchangerate-API."
    )
    sendEmail(crypto_msg)
else:
    # Send error message if data not fetched
    failure_msg = ("Subject:Could Not Send Crypto Data\n\n"
                   "Check Your Code. There is some error preventing it from working!")
    sendEmail(msg=failure_msg)