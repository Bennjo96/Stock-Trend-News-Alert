# Name: Benjamin Mahello
# Final Project Name: Stock Trend News Alert
# School : Redi School 2021


import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "S9J5UKF3QX645F7P"
NEWS_API_KEY = "147494cf245d48969d69c8e0acc471e0"
TWILIO_SID = "AC1fa39cec7e6ec849c5a5385bc023f674"
TWILIO_AUTH_TOKEN = "1411819dd99d0e5753d72ec6a12540fd"

# STEP 1: I Used https://www.alphavantage.co/documentation/#daily API
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then will print("Get News").

# Getting yesterday's closing stock price
stock_params = {  # Stock Parameters
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,  # stock symbol TSLA
    "apikey": STOCK_API_KEY,  # stock API Key
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)  # Fetch from Stock Endpoint
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]  # List Comprehension changing dictionary to list
yesterday_data = data_list[0]  # Fetching from yesterday data at index 0
yesterday_closing_price = yesterday_data["4. close"]  # Fetching Closing Price
print(f"{yesterday_closing_price} :Yesterday Closing Price ")  # Printing yesterday's closing stock price

# Getting the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]  # Fetching from yesterday data at index 1
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]  # Fetching before yesterday Closing Price
print(f"{day_before_yesterday_closing_price} : day before yesterday closing price")  # Printing day before yesterday
# closing stock price

# Find the positive difference between Step 1 and Step 2. by Python abs() Function
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(f"{diff_percent}% : Percentage Difference in Price")

# STEP 2:
# If difference percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 1: # Here i used the least number as 1 when testing, but we can use 5 too.
    news_params = {
        "apiKey": NEWS_API_KEY,  # using news API to get Article related to the Company name
        "qInTitle": COMPANY_NAME,  # Query and title we are searching for.
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Using Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]  # Fetching Top 3 Articles from News API
    print(three_articles)  # Printing Out Response as Json

    # STEP 3: Using Twilio to send a seperate message with each article's title and description to my phone number.
    # Creating a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]

    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Sending each article as a separate message via Twilio. ** Am unable to receive the message Because am suppose
    # to upgrade Twilio to Payable version in Order to get Notification
    for article in formatted_articles:  # Inorder to send 3 Messages I have loop Through Formatted Articles
        message = client.messages.create(
            body=article,
            from_="+17045503933",  # VIRTUAL_TWILIO_NUMBER
            to="+4915217032349"  # VERIFIED_NUMBER
        )
