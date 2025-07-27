
# Crypto-Price-Tracker

Crypto-Price-Tracker is a Python tool that tracks your crypto portfolio using CoinGecko and ExchangeRate APIs. It calculates profit/loss in USD and PKR, and sends daily performance reports via email using SendGrid.

## API Reference

#### Get all items

```http
  GET https://api.coingecko.com/api/v3/simple/price
```

| Parameter       | Type     | Description                                                                 |
| :-------------- | :------- | :-------------------------------------------------------------------------- |
| `ids`           | `string` | **Required**. Comma-separated coin IDs like `bitcoin,ethereum,solana,litecoin` |
| `vs_currencies` | `string` | **Required**. The fiat currency to convert into (e.g., `usd`)              |

#### Get item

```http
  GET https://v6.exchangerate-api.com/v6/${EXCHANGE_API_KEY}/latest/USD
```

| Parameter          | Type     | Description                              |
| :----------------- | :------- | :--------------------------------------- |
| `EXCHANGE_API_KEY` | `string` | **Required**. Your API key from exchangerate-api.com |## Authors

- [@Muhammad-Ali](https://github.com/Muhammad-Ali-5331)
## Appendix

- Data fetched from [CoinGecko API](https://www.coingecko.com/en/api) for live crypto prices.
- Exchange rates provided by [Exchangerate-API](https://www.exchangerate-api.com/).
- Emails sent securely using [SendGrid](https://sendgrid.com/).
- Hosted automation example: [PythonAnywhere](https://www.pythonanywhere.com/).
- Developed and maintained by [@Muhammad-Ali-5331](https://github.com/Muhammad-Ali-5331).
## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![SendGrid API](https://img.shields.io/badge/Email-SendGrid-blue)](https://sendgrid.com/)
[![ExchangeRate API](https://img.shields.io/badge/API-ExchangeRate-purple)](https://www.exchangerate-api.com/)
[![CoinGecko API](https://img.shields.io/badge/API-CoinGecko-orange)](https://www.coingecko.com/en/api)
## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

### 🔐 SendGrid Email API Configuration (Used in this project)

`SEND_GRID_API` — Your SendGrid API key  
`SENDER_EMAIL` — Your verified SendGrid sender email  
`RECEIVER_EMAIL` — Recipient email address  

### 🌐 Exchange Rate API

`EXCHANGE_API_KEY` — Your ExchangeRate API key  

### 💸 Investment Configuration

`BTC_PURCHASE_PRICE` — Purchase price of Bitcoin in PKR  
`ETH_PURCHASE_PRICE` — Purchase price of Ethereum in PKR  
`SOL_PURCHASE_PRICE` — Purchase price of Solana in PKR  
`LTC_PURCHASE_PRICE` — Purchase price of Litecoin in PKR  

`BTC_INVESTED` — Amount of USD invested in Bitcoin  
`ETH_INVESTED` — Amount of USD invested in Ethereum  
`SOL_INVESTED` — Amount of USD invested in Solana  
`LTC_INVESTED` — Amount of USD invested in Litecoin  

`USD_PURCHASED_PRICE` — PKR rate per USD at time of purchase  

---

### 📨 SMTP Email Configuration — *Only use this if switching to SMTP instead of SendGrid*

`SMTP_SERVER` — Your SMTP server (e.g., smtp.gmail.com)  
`SMTP_PORT` — SMTP port (e.g., 587)  
`EMAIL_USERNAME` — Your email address  
`EMAIL_PASSWORD` — Your app password or email password (use app password for Gmail)
## Documentation

[Full Project Documentation](https://github.com/Muhammad-Ali-5331/Crypto-Price-Tracker#readme)## FAQ

#### Why is my email going to spam?
Emails sent via services like SendGrid may land in spam due to sender reputation, content, or unverified domains. Always verify your sender email in SendGrid and avoid spammy content.

#### Can I use my university email (e.g., bsef23a021@pucit.edu.pk)?
You can, but university domains may have stricter filters. It's better to use a verified personal Gmail or domain-based email for higher deliverability.

#### How do I load a specific `.env` file from a different folder?
You can use `dotenv.load_dotenv('../sendgrid.env')` to load env vars from the parent directory.

#### What's the difference between SendGrid and SMTP variables?
- **SendGrid**: Uses `SENDGRID_API_KEY`, `SENDER_EMAIL`, `RECEIVER_EMAIL`.
- **SMTP (e.g., Gmail)**: Uses `SMTP_USER`, `SMTP_PASS`, `SMTP_SERVER`, `SMTP_PORT`.

#### What APIs does this project use?
- [CoinGecko](https://www.coingecko.com/en/api) for live crypto prices.
- [Exchangerate-API](https://www.exchangerate-api.com/) for USD to PKR exchange rate.
## Features

- 📊 Daily automatic crypto portfolio tracking
- 💱 Live USD to PKR conversion using real-time exchange rates
- 🪙 Individual P/L tracking for BTC, ETH, SOL, LTC
- 📧 Auto email reports using SendGrid API
- 🔐 Environment-based secure credentials (.env support)
- 📁 Deployable on PythonAnywhere or any cloud platform
- ⏱️ Scheduled execution with accurate time logging
- ✅ Clean, readable HTML email formatting
## Lessons Learned

While building this Crypto Price Tracker, I learned how to integrate multiple APIs (CoinGecko and ExchangeRate-API) to fetch real-time financial data. I also explored sending dynamic HTML email reports using SendGrid and handling environment variables securely with `.env` files. 

A major challenge was ensuring accurate currency conversion and calculating profits after deducting platform fees. Another was dealing with email delivery issues like spam filtering, which I addressed through verified domains and cleaner HTML structure.

This project helped me understand the importance of automation, modular coding practices, and platform compatibility when scheduling recurring scripts.
## Installation

To install and run the Crypto Price Tracker locally using Python, follow these steps:

```bash
git clone https://github.com/Muhammad-Ali-5331/Crypto-Price-Tracker.git
cd Crypto-Price-Tracker
pip install -r requirements.txt

## Support

For support, email malitariq5324@gmail.com or open an issue on [GitHub](https://github.com/Muhammad-Ali-5331/Crypto-Price-Tracker/issues).
