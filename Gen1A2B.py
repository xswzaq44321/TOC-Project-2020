from utils import send_text_message
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
import random

Game1A2B_N = 4


def genStates(n):
    states = ["play_1A2B", ]
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    name = 'state_1A2B_%d%d%d%d' % (i, j, k, l)
                    states.append(name)
                    states.append(name + "correct")
                    states.append(name + "wrong")
    states.append("state_1A2B_winning")
    return states


def genTransitions(root, n):
    transitions = []
    transitions.append({
        "trigger": "advance",
        "source": root,
        "dest": "play_1A2B",
        "conditions": "is_going_to_play_1A2B"
    })
    objBack = {
        "source": [],
        "trigger": "advance",
        "dest": "play_1A2B",
        "conditions": "is_going_to_replay_1A2B"
    }
    objExit = {
        "source": [],
        "trigger": "advance",
        "dest": root,
        "conditions": "is_going_to_quit_1A2B"
    }
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    dest = 'state_1A2B_%d%d%d%d' % (i, j, k, l)
                    trigger = 'go_to_%s' % dest
                    conditions = 'is_going_to_%s' % dest
                    obj = {
                        "source": "play_1A2B",
                        "trigger": trigger,
                        "dest": dest
                        # "conditions": conditions
                    }
                    transitions.append(obj)
                    objBack['source'].append(dest)
                    objExit['source'].append(dest)
                    objCorrect = {
                        "trigger": "advance",
                        "source": dest,
                        "dest": dest + "correct",
                        "conditions": conditions + "correct"
                    }
                    objWrong = {
                        "trigger": "advance",
                        "source": dest,
                        "dest": dest + "wrong",
                        "conditions": conditions + "wrong"
                    }
                    transitions.append(objCorrect)
                    transitions.append(objWrong)
                    objCorrectBack = {
                        "trigger": "go_to_winning",
                        "source": dest + "correct",
                        "dest": "state_1A2B_winning"
                    }
                    objWrongBack = {
                        "trigger": "back_from_%s" % (dest + "wrong"),
                        "source": (dest + "wrong"),
                        "dest": dest
                    }
                    transitions.append(objCorrectBack)
                    transitions.append(objWrongBack)
    transitions.append(objBack)
    print(objBack['source'])
    transitions.append(objExit)
    transitions.append({
        "trigger": "advance",
        "source": "state_1A2B_winning",
        "dest": "play_1A2B",
        "conditions": "is_play_again_1A2B",
    })
    transitions.append({
        "trigger": "advance",
        "source": "state_1A2B_winning",
        "dest": root,
        "conditions": "is_exit_1A2B"
    })
    return transitions


def checkAB(ans, guess):
    A = 0
    B = 0
    matchedGuess = [False] * len(ans)
    matchedAns = [False] * len(ans)
    if(not isinstance(guess, int) or len(guess) != len(ans)):
        return 'Nani the fuck?'
    print(guess, range(0, Game1A2B_N))
    for i in range(len(guess)):
        if(int(guess[i]) not in range(0, Game1A2B_N)):
            return 'Number out of range [0~%d].' % (Game1A2B_N - 1)
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

    def is_going_to_play_1A2B(self, event):
        text = event.message.text
        return text.lower() == "play 1a2b"

    def on_enter_play_1A2B(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, TextSendMessage(
            "Let's play 1A2B.\nRange [0~%d]*4." % (Game1A2B_N - 1)))
        comb = "%d%d%d%d" % (random.randint(0, n - 1), random.randint(0, n - 1),
                             random.randint(0, n - 1), random.randint(0, n - 1))
        print("1A2B answer =", comb)
        getattr(self, "go_to_state_1A2B_%s" % comb)(event)

    def is_going_to_replay_1A2B(self, event):
        text = event.message.text
        return text.lower() == "replay"

    def is_going_to_quit_1A2B(self, event):
        text = event.message.text
        return text.lower() == "quit"
    handlers.append({
        "is_going_to_replay_1A2B": is_going_to_replay_1A2B
    })
    handlers.append({
        "is_going_to_quit_1A2B": is_going_to_quit_1A2B
    })
    handlers.append({
        "is_going_to_play_1A2B": is_going_to_play_1A2B
    })
    handlers.append({
        "on_enter_play_1A2B": on_enter_play_1A2B
    })
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                for l in range(0, n):
                    comb = '%d%d%d%d' % (i, j, k, l)
                    dest = 'state_1A2B_%s' % comb
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

                    # correct handle
                    destCorrect = dest + "correct"
                    is_going_to_correct = 'is_going_to_%s' % destCorrect

                    def is_going_to_correct_gen(comb):
                        def foo(self, event):
                            text = event.message.text
                            # print(checkAB(text.lower()) == '4A0B')
                            return checkAB(comb, text.lower()) == '4A0B'
                        return foo
                    is_going_to_correct_foo = is_going_to_correct_gen(comb)
                    on_enter_correct = 'on_enter_%s' % destCorrect

                    def on_enter_correct_gen():
                        def foo(self, event):
                            reply_token = event.reply_token
                            button_message = TemplateSendMessage(
                                alt_text='Button',
                                template=ButtonsTemplate(
                                    thumbnail_image_url='https://i.imgur.com/eU7uJAJ.jpg',
                                    image_aspect_ratio="rectangle",
                                    image_size="contain",
                                    title='再來一次?',
                                    text='Please select',
                                    actions=[
                                        MessageAction(
                                            label='Yes',
                                            text='Yes'
                                        ),
                                        MessageAction(
                                            label='No',
                                            text='No'
                                        ),
                                    ]
                                )
                            )
                            send_text_message(reply_token, button_message)
                            self.go_to_winning(event)
                        return foo
                    on_enter_correct_foo = on_enter_correct_gen()
                    on_exit_correct = 'on_exit_%s' % destCorrect

                    def on_exit_correct_foo(self, event):
                        pass
                    handlers.append({
                        is_going_to_correct: is_going_to_correct_foo,
                        on_enter_correct: on_enter_correct_foo,
                        on_exit_correct: on_exit_correct_foo,
                    })

                    # wrong handle
                    destWrong = dest + "wrong"
                    is_going_to_wrong = 'is_going_to_%s' % destWrong

                    def is_going_to_wrong_gen(comb):
                        def foo(self, event):
                            text = event.message.text
                            if (text.lower() == "replay"):
                                return False
                            elif(text.lower() == "quit"):
                                return False
                            return checkAB(comb, text.lower()) != '4A0B'
                        return foo
                    is_going_to_wrong_foo = is_going_to_wrong_gen(comb)
                    on_enter_wrong = 'on_enter_%s' % destWrong

                    def on_enter_wrong_gen(comb, destWrong):
                        def foo(self, event):
                            text = event.message.text
                            reply_token = event.reply_token
                            result = checkAB(comb, text.lower())
                            send_text_message(
                                reply_token, TextSendMessage(text=result))
                            getattr(
                                self, "back_from_%s" % destWrong)(event)
                        return foo
                    on_enter_wrong_foo = on_enter_wrong_gen(comb, destWrong)
                    on_exit_wrong = 'on_exit_%s' % destWrong

                    def on_exit_wrong_foo(self, event):
                        pass
                    handlers.append({
                        is_going_to_wrong: is_going_to_wrong_foo,
                        on_enter_wrong: on_enter_wrong_foo,
                        on_exit_wrong: on_exit_wrong_foo,
                    })

    def is_play_again_1A2B(self, event):
        text = event.message.text
        return text.lower() == "yes"

    def is_exit_1A2B(self, event):
        text = event.message.text
        return text.lower() == "no"
    handlers.append({
        "is_play_again_1A2B": is_play_again_1A2B
    })
    handlers.append({
        "is_exit_1A2B": is_exit_1A2B
    })
    return handlers


# with open("output.py", "w") as f:
#     f.write(str(genTransitions("user", 5)))
