import requests
import datetime as dt
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

# To automate your code through PythonAnywhere
# proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_API = "API_KEY"
alpha_url = "https://www.alphavantage.co/query"

account_sid = "AC0c58ed57ae5a93f8898922f1a2b66238"
auth_token = "API_KEY"

NEWS_API = "API_KEY"
news_url = "https://newsapi.org/v2/everything"

alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API
}
twilio_number = "+12568874894"

response = requests.get(alpha_url, params=alpha_params)
response.raise_for_status()
stock_data = response.json()['Time Series (Daily)']
stock_values = [value for (key, value) in stock_data.items()]

yesterday_before_close = float(stock_values[1]['4. close'])
yesterday_close = float(stock_values[0]['4. close'])
percentage = round(((yesterday_close - yesterday_before_close) / yesterday_close) * 100, 2)

news_params = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME
}
news_response = requests.get(news_url, params=news_params)
news_response.raise_for_status()
top_headlines = news_response.json()
news = [value for (key, value) in top_headlines.items()]
for index in range(3):
    news_title = news[2][index]['title']
    news_description = news[2][index]['description']
    news_url = news[2][index]['url']
    if percentage > 0:
        emoji = "🔺"
    else:
        emoji = "🔻"
    client = Client(account_sid, auth_token
#             To automate your code through PythonAnywhere
#                     , http_client=proxy_client
                   )
    message = client.messages \
        .create(
        body=f"{STOCK}: {emoji} {abs(percentage)}%\n"
             f"Headline: {news_title}\n"
             f"Brief: {news_description}\n"
             f"For full story: {news_url}",
        from_=twilio_number,
        to='+YOURNUMBER'
    )

    print(message.status)
