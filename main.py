import requests
import datetime as dt
from datetime import datetime, timedelta
from twilio.rest import Client

# ---------------------- INSTRUCTIONS ---------------------- #

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

# ---------------------- VARIABLES SET UP ---------------------- #
account_sid = ""
auth_token = ""

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "http://api.marketstack.com/v1/eod"
STOCK_API_KEY = ""

today = dt.datetime.now()
today_date = str(today).split(" ")[0]

if today.weekday() == 0:
    last_business_day = datetime.today() - timedelta(days=2)
    two_business_days_before = datetime.today() - timedelta(days=3)
elif today.weekday() == 1:
    last_business_day = datetime.today() - timedelta(days=3)
    two_business_days_before = datetime.today() - timedelta(days=4)
elif today.weekday() == 2:
    last_business_day = datetime.today() - timedelta(days=1)
    two_business_days_before = datetime.today() - timedelta(days=4)
elif today.weekday() in (3, 4, 5, 6):
    last_business_day = datetime.today() - timedelta(days=1)
    two_business_days_before = datetime.today() - timedelta(days=2)

last_business_day_date = str(last_business_day).split(" ")[0]
two_business_days_before_date = str(two_business_days_before).split(" ")[0]

stock_params = {
    'access_key': STOCK_API_KEY,
    'symbols': STOCK_NAME,
    'date_from': two_business_days_before_date,
    'date_to': last_business_day_date,
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "20b2c76ce12a4404b1377ddf5517b3df"

news_params = {
    'q': COMPANY_NAME,
    'apiKey': NEWS_API_KEY,
    'language': 'en',
    'from': two_business_days_before,
    'to': today_date,
}

# ---------------------- FUNCTIONS SET UP ---------------------- #
def stockAnalysis(STOCK_2days_ago, STOCK_yesterday):
    if STOCK_yesterday < STOCK_2days_ago:
        percentage = (100 - ((STOCK_yesterday * 100) / STOCK_2days_ago))
        results = ['decreace', round(percentage, 2)]

    elif STOCK_2days_ago < STOCK_yesterday:
        percentage = (((STOCK_yesterday * 100) / STOCK_2days_ago) - 100)
        results = ['increace', round(percentage, 2)]

    elif STOCK_2days_ago == STOCK_yesterday:
        percentage = STOCK_2days_ago - STOCK_yesterday
        results = ['no diference', round(percentage, 2)]

    return results


# ---------------------- CODE  ---------------------- #

"""
# Stock days not working, possible solution
I'M TOO TIRED BUT...

320. Solution & Walkthrough for Step 1 - Check for Stock Price Movements/Q&A/aaarrrrgggghhh (arg? ;-) Nerd Alert/Thor Vadstein 2022:
    A slightly shorter version (and more clear?) of what Angela shows in the videos is this:
        stock_result = requests.get(url=ALPHA_URL, params=ALPHA_PARAMS).json()["Time Series (Daily)"]
        stock_dates = list(stock_result)[:2] 
        close_yesterday = float(stock_result[stock_dates[0]]["4. close"])
        close_prev_day = float(stock_result[stock_dates[1]]["4. close"])
    No need to worry about dates, as the stock_dates will contain a list of the two most recent.
"""

STOCK_response = requests.get(STOCK_ENDPOINT, params=stock_params)
print(STOCK_response.json())

#STOCK_2days_ago = STOCK_response.json()['data'][0]['close']
#STOCK_yesterday = STOCK_response.json()['data'][1]['close']

STOCK_2days_ago = 157.67
STOCK_yesterday = 167.67

stockAnalysis_result = stockAnalysis(STOCK_2days_ago, STOCK_yesterday)

print(stockAnalysis_result)

if 5 < stockAnalysis_result[1]:
    print('Get News')

NEWS_response = requests.get(NEWS_ENDPOINT, params=news_params)
#print(NEWS_response.json())

articles = []
for i in range(0, 3):
    articles.append(
        {
            "title": NEWS_response.json()["articles"][i]["title"],
            "content": NEWS_response.json()["articles"][i]["content"],
            "url": NEWS_response.json()["articles"][i]["url"],
        }
    )
print(articles)

if stockAnalysis_result[0] == 'increace':
    stocks_alert = f"TSLA: 🔺{stockAnalysis_result[1]}%"
elif stockAnalysis_result[0] == 'decreace':
    stocks_alert = f"TSLA: 🔻{stockAnalysis_result[1]}%"

for item in articles:
    stocks_alert += f"""
    Headline: {articles[articles.index(item)]['title']}
    Brief: {articles[articles.index(item)]['content']}
    {articles[articles.index(item)]['url']}
    """
print(stocks_alert)

client = Client(account_sid, auth_token)
message = client.messages \
    .create(
    body = f"{stocks_alert}",
    from_= "+16294683691",
    to = "+525529903445"
)
print(message.status)

