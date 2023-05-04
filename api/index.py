from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('NOcgdu2y7bY33vjfhzYdP+zJty8MNSI5VQ8sq5kX9jF6r1r78zdmznZmGXGUbX6ng1EfZiHRSNvnQMl9ZCb5hv0XlOoIFoJHd6FTa4NpsQcur+vBD1XEsgCNrEGQsT1U6IPjBpW/KjFcUvrKkMt8ggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6713982daf78e7b1af160954fde0cc6e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()