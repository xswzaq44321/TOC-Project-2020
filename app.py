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
    states=["user"] + Gen1A2B.genStates(Gen1A2B.Game1A2B_N),
    transitions=[] + Gen1A2B.genTransitions("user", Gen1A2B.Game1A2B_N),
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


def makeTocMachine(N):
    return TocMachine(
        states=["user"] + Gen1A2B.genStates(N),
        transitions=[] + Gen1A2B.genTransitions("user", N),
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )


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


userMachines = dict()


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
        user_id = event.source.user_id
        if (user_id not in userMachines):
            userMachines[user_id] = makeTocMachine(Gen1A2B.Game1A2B_N)
        userMachine = userMachines[user_id]
        print(f"\nFSM STATE: {userMachine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = userMachine.advance(event)
        if response == False:
            send_text_message(event.reply_token, TextSendMessage(
                text="我看不懂QQ"))

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
