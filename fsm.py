from transitions.extensions import GraphMachine

from utils import send_text_message
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
import Gen1A2B


class Game1A2B:
    pass


for obj in Gen1A2B.genHandlers(Gen1A2B.Game1A2B_N):
    for k, v in obj.items():
        print(k, v)
        setattr(Game1A2B, k, v)


class TocMachine(Game1A2B, GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_play_1A2B(self, event):
        text = event.message.text
        return text.lower() == "play 1a2b"

    def on_enter_play_1A2B(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, TextSendMessage("Let's play 1A2B"))
        self.go_to_state_1A2B_0000(event)

    # def is_going_to_state_1A2B_00000000(self, event):
    #     return False

    # def is_going_to_state_1A2B_00000001(self, event):
    #     return True

    # def on_enter_state_1A2B_00000001(self, event):
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
