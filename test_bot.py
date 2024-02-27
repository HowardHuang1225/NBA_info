from flask_ngrok import run_with_ngrok
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

app = Flask(__name__)

@app.route("/")
def home():
  line_bot_api = LineBotApi('qLqJwcq/hvCwu8u32stf0dmgQTr51T+DV/d4BN8FhXyjjiJTrMrRtQj0UydgunkMJDhuePzMGtFol+RRY1qsl2VfVKJlsOY8a94vlTzJDP6+NNuVcvyeK1Yfh29bAfNDnvAA1gITB3yRz2p7o2iAwgdB04t89/1O/w1cDnyilFU=')
  try:
    # 網址被執行時，等同使用 GET 方法發送 request，觸發 LINE Message API 的 push_message 方法
    line_bot_api.push_message('U3de2e6e5c37b4b02713a017ee9104086', TextSendMessage(text='Hello World!!!'))
    return 'OK'
  except:
    print('error')

if __name__ == "__main__":
    run_with_ngrok(app)
    app.run()