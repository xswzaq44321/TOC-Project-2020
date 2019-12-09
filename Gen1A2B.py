from utils import send_text_message
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction

Game1A2B_N = 2


def genStates(n):
    states = []
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    name = 'state_1A2B_%d%d%d%d' % (i, j, k, l)
                    states.append(name)
                    for a in range(0, n):
                        for b in range(0, n):
                            for c in range(0, n):
                                for d in range(0, n):
                                    states.append(name + '%d%d%d%d' %
                                                  (a, b, c, d))
    return states


def genTransitions(root, n):
    transitions = []
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    obj = {
                        "source": root,
                    }
                    dest = 'state_1A2B_%d%d%d%d' % (i, j, k, l)
                    trigger = 'go_to_%s' % dest
                    conditions = 'is_going_to_%s' % dest
                    obj['trigger'] = trigger
                    obj['dest'] = dest
                    # obj['conditions'] = conditions
                    transitions.append(obj)
                    for a in range(0, n):
                        for b in range(0, n):
                            for c in range(0, n):
                                for d in range(0, n):
                                    obj2 = {
                                        "trigger": "advance",
                                        "source": dest,
                                    }
                                    dest2 = dest + '%d%d%d%d' % (a, b, c, d)
                                    conditions2 = conditions + \
                                        '%d%d%d%d' % (a, b, c, d)
                                    obj2['dest'] = dest2
                                    obj2['conditions'] = conditions2
                                    transitions.append(obj2)
                                    obj2Back = {
                                        "trigger": "back_from_%s" % dest2,
                                        "source": dest2,
                                        "dest": dest
                                    }
                                    transitions.append(obj2Back)
    return transitions


with open("output.py", "w") as w:
    w.write(str(genTransitions("play_1A2B", 2)))


def checkAB(ans, guess):
    A = 0
    B = 0
    matchedGuess = [False, False, False, False]
    matchedAns = [False, False, False, False]
    for i in range(len(guess)):
        if (guess[i] == ans[i]):
            A = A + 1
            matchedGuess[i] = True
            matchedAns[i] = True
    for i in range(len(guess)):
        if (matchedGuess[i]):
            continue
        for j in range(len(ans)):
            if (guess[i] == ans[j] and not matchedAns[j]):
                B = B + 1
                matchedGuess[i] = True
                matchedAns[j] = True
                break
    return '%dA%dB' % (A, B)


def genHandlers(n):
    handlers = []
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    comb = '%d%d%d%d' % (i, j, k, l)
                    dest = 'state_1A2B_%s' % comb
                    # is_going_to = 'is_going_to_%s' % dest

                    # def is_going_to_foo(self, event):
                    #     text = event.message.text
                    #     return text.lower() == comb
                    on_enter = 'on_enter_%s' % dest

                    def on_enter_foo(self, event):
                        pass
                    on_exit = 'on_exit_%s' % dest

                    def on_exit_foo(self, event):
                        pass
                    handlers.append({
                        # 'dest': dest,
                        on_enter: on_enter_foo,
                        on_exit: on_exit_foo,
                    })
                    for a in range(0, n):
                        for b in range(0, n):
                            for c in range(0, n):
                                for d in range(0, n):
                                    guess = '%d%d%d%d' % (a, b, c, d)
                                    dest2 = dest + guess
                                    is_going_to2 = 'is_going_to_%s' % dest2

                                    def is_going_to2_gen(guess):
                                        def faa(self, event):
                                            text = event.message.text
                                            print(text.lower() == guess)
                                            return text.lower() == guess
                                        return faa
                                    is_going_to2_foo = is_going_to2_gen(guess)
                                    on_enter2 = 'on_enter_%s' % dest2

                                    def on_enter2_gen(comb, dest2):
                                        def foo(self, event):
                                            text = event.message.text
                                            result = checkAB(text, comb)
                                            print('on_enter2_foo', text)
                                            if (result == '4A0B'):
                                                reply_token = event.reply_token
                                                send_text_message(
                                                    reply_token, TextSendMessage(text="You won!:D"))
                                            else:
                                                reply_token = event.reply_token
                                                send_text_message(
                                                    reply_token, TextSendMessage(text=result))
                                                getattr(
                                                    self, "back_from_%s" % dest2)(event)
                                        return foo
                                    on_enter2_foo = on_enter2_gen(comb, dest2)
                                    on_exit2 = 'on_exit_%s' % dest2

                                    def on_exit2_foo(self, event=None):
                                        pass
                                    handlers.append({
                                        # 'dest': dest2,
                                        is_going_to2: is_going_to2_foo,
                                        on_enter2: on_enter2_foo,
                                        on_exit2: on_exit2_foo,
                                    })
    return handlers


# with open("output.py", "w") as f:
#     f.write(str(genTransitions("user", 5)))
