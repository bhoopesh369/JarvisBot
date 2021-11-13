import telebot
import yfinance as yf
from PIL import Image
import requests
from io import BytesIO
import random
import praw

TOKEN = "2089092326:AAEmGJZwscquf99EMpgQuY89omPfqHMacks"
bot = telebot.TeleBot(TOKEN)

Image_Link="https://source.unsplash.com/random/300x200?sig=${Math.random()}.jpg"


reddit = praw.Reddit(client_id="VKeB6HMwelofNSqZU1EgjQ",
                     client_secret="uuGNN3YwmqgSpUk38BYChpum_L6q7A",
                     username="Historical_Cash_5628",
                     password="bjioknmlp",  
                     user_agent="this is useless")

def get_post(rddt, sbrddt, first_x_posts=100):
    subreddit = rddt.subreddit(sbrddt)  # Get the subreddit
    hot = subreddit.hot(limit=first_x_posts)  # Get the first 100 posts
    post = random.choice(list(hot))  # Get a random post from them
    return post


@bot.message_handler(commands=['start'])
def start(message):
  print(message.text)

@bot.message_handler(commands=['greet','hello','hi'])
def hello(message):
  bot.send_message(message.chat.id, "Hey! Hows it going?")

@bot.message_handler(commands=['image','img'])
def image(message):
  img = open("cat.jpg", "rb")
  bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=["randimg",'imgnet'])
def imagenet(message):
  response= requests.get(Image_Link)
  imgnet= Image.open(BytesIO(response.content))
  bot.send_photo(message.chat.id, imgnet)

@bot.message_handler(commands=['vid','video'])
def video(message):
  vid= open("GPNAKKU.mp4", "rb")
  bot.send_video(message.chat.id,vid)

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amzn','TTM','nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 3)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print() 

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)
  
def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True 
@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='30m', interval='5m')
  if data.size > 0:
    data=data.reset_index()
    data["format_date"]=data['Datetime'].dt.strftime('%m/%d   %I:%M %p') 
    data.set_index('format_date',inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No Data!?")
  pass


@bot.message_handler(commands=["reddit", "r"])
def send_post(message):
    post = get_post(rddt=reddit, sbrddt="askreddit")
    try:
        response = requests.get(post.url)
        img = Image.open(BytesIO(response.content))
        bot.send_photo(message.chat.id, img, caption=post.title)
    except Exception as e:
        if "cannot identify image file <_io.BytesIO object at" in str(e):
         bot.send_message(message.chat.id, f"{post.url}\n{post.title}")


bot.polling() 
