import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message
import Gen1A2B

load_dotenv()

machine = TocMachine(
    states=["user", "play_1A2B"] + Gen1A2B.genStates(Gen1A2B.Game1A2B_N),
    transitions=[
        {"trigger": "advance", "source": "user", "dest": "play_1A2B",
            "conditions": "is_going_to_play_1A2B"},
    ]
    + Gen1A2B.genTransitions("play_1A2B", Gen1A2B.Game1A2B_N),
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

# for obj in Gen1A2B.genHandlers(N):
#     for k, v in obj.items():
#         setattr(TocMachine, k, v)
#         print(k, v)

print(hasattr(machine, 'is_going_to_state_1A2B_00000001'))

# def foo(self, event):
#     text = event.message.text
#     result = '4A0B'
#     print('on_enter2_foo', text)
#     if (result == '4A0B'):
#         reply_token = event.reply_token
#         send_text_message(
#             reply_token, TextSendMessage(text="You won!:D"))
#     else:
#         reply_token = event.reply_token
#         send_text_message(
#             reply_token, TextSendMessage(text=result))


# setattr(TocMachine, 'on_enter_state1A2B_00000001', foo)

# TocMachine.on_enter_state_1A2B_00000001(None, None)

# setattr(TocMachine, 'is_going_to_state3', is_going_to_state3)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, TextSendMessage(
                text="Not Entering any State"))

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
