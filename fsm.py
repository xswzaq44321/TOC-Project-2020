from transitions.extensions import GraphMachine

from utils import send_text_message
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
import Gen1A2B


class Game1A2B:
    pass


for obj in Gen1A2B.genHandlers(Gen1A2B.Game1A2B_N):
    for k, v in obj.items():
        # print(k, v)
        setattr(Game1A2B, k, v)


class TocMachine(Game1A2B, GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
