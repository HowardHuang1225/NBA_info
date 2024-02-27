from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, ImageMessage, VideoMessage, TextSendMessage
)
import configparser
import random
import requests
from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
import datetime
from datetime import datetime as dt
from nba_info import get_games_info, complete_games



def is_valid_date(input_date):
    try:
        dt.strptime(input_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False



app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=(TextMessage, StickerMessage, ImageMessage, VideoMessage))
def pretty_echo(event):
    note = ["你要今日賽程嗎?!","想要看比賽熱血沸騰嗎?!","想看球嗎?!","手癢了嗎?!"]
    if event.source.user_id != "0979974760":
        if isinstance(event.message, TextMessage):
            if event.message.text=="NBA" or event.message.text=="Ball" or event.message.text=="nba" or event.message.text=="Nba" or event.message.text=="nBa" or event.message.text[0:3] =="Nba" or event.message.text[0:3] =="nba" or event.message.text[0:3] == "NBA" or event.message.text[0:2] =="籃球":
                games_info = get_games_info(dt.now().strftime("%Y-%m-%d"))
                pretty_text =f"今日賽程！\n{games_info}"
            elif  event.message.text=="Game" or event.message.text=="game" or event.message.text=="GAME"  or event.message.text[0:4] =="Game" or event.message.text[0:4] =="game" or event.message.text[0:4] =="GAME":
                games_info = complete_games(dt.now().strftime("%Y-%m-%d"))
                pretty_text =f"今日比賽結果！\n{games_info}"
            elif event.message.text=="TIME" or event.message.text=="time" or event.message.text=="Time"  or event.message.text[0:4] =="TIME" or event.message.text[0:4] =="time" or event.message.text[0:4] =="Time":
                pretty_text = "上連結: https://nba.hupu.com/schedule"

            elif event.message.text=="WATCH" or event.message.text=="watch" or event.message.text=="Watch"  or event.message.text[0:5] =="WATCH" or event.message.text[0:5] =="watch" or event.message.text[0:5] =="Watch":
                pretty_text = "上連結: http://www.88kanqiu.me/match/1/live"
            elif event.message.text=="Help" or event.message.text=="help" or event.message.text=="HELP"  or event.message.text[0:4] =="Help" or event.message.text[0:4] =="help" or event.message.text[0:4] =="HELP":
                pretty_text = '''關鍵字:\nnba: 今日賽程\ngame: 今日賽況\ntime: 今日比賽時程\nwatch: 比賽直播連結\n輸入日期yyyy-mm-dd: 查詢當日賽程'''
            elif is_valid_date(event.message.text):
                games_info = get_games_info(event.message.text)
                pretty_text =f"賽程如下！\n{games_info}"
            else:
                pretty_text = random.choice(note) + "跟我說 NBA !!!"
        else:
            pretty_text = random.choice(note)+"跟我說 NBA !!!"

        send_messages = [
            TextSendMessage(text=pretty_text)
        ]
        
        # send_messages.append(TextSendMessage(text="Hello hahahahhahahahha"))
        

        line_bot_api.reply_message(
            event.reply_token,
            send_messages
        )

        

        

if __name__ == "__main__":
    app.run()