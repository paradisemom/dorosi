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

line_bot_api = LineBotApi('c83lIj1OeWi7+euqicb37C4AUnN6angPnFAXILyRSuy4uFEOtJAlXjNj1rWmbKkVxOH7ZGVBcMZsd70eWD2zZVFueXeLpNrjI0jSVX/koCO+fdtgB2OoUS+ReAclsvmuh+lIO4ya1sxVaE3AJY7atQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f526628eabf9391d9c5f49f40f186bff')


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