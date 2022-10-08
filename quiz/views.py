import pdb
from django.http import HttpResponse
import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from quiz.models import Choice, User, Quiz

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ButtonsTemplate,
    FollowEvent,
    TemplateSendMessage,
    MessageAction,
)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@csrf_exempt
def health_check(request):

    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def callback(request):

    if request.method == "POST":

        # get X-Line-Signature header value
        import json

        signature = request.headers["X-Line-Signature"]
        # body = json.loads(request.body.decode('utf-8'))

        # get request body as text
        body = request.body.decode("utf-8")

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print(
                "Invalid signature. Please check your channel access token/channel secret."
            )

    return HttpResponse("Done")


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user = User.objects.get(user_id=event.source.user_id)

    def extract_answer(message) -> Choice:
        # messageがChoiceのtextにperfect matchするかどうかを確認する
        # XXX: 全てのChoiceをUniqueにする必要がある。
        choice = Choice.objects.filter(text=message)
        if len(choice) != 1:
            # 雑談が挟まれたら、写真などを返す？
            return None
        else:
            return choice[0]

    choice = extract_answer(event.message.text)
    if choice is None:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ちょっと何言ってるか良くわからない。")
        )
    else:
        # 問題に対する回答の場合は、合っていたら加点する
        # XXX:
        # これだと同じ回答を送り続けるとチートできてしまうわ
        user.score += choice.is_correct
        user.save()

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="回答有難うございます！")
        )


# register uuids and names
@handler.add(FollowEvent)
def add_follower(event):
    """follow eventが発生したタイミングで起動する"""

    # クイズをPUSH送信するためにuuidsを保存
    participant_userId = event.source.user_id
    # extract user name from user profile

    try:
        profile = line_bot_api.get_profile(participant_userId)
        name = profile.display_name
    except LineBotApiError as e:
        # エラーハンドリング
        pass
    # save users
    User(user_id=participant_userId, name=name).save()

    # フォロー有難う！とメッセージを返す
    line_bot_api.push_message(
        to=participant_userId, messages=TextSendMessage(text=f"フォロー有難うございます！{name}")
    )


def push_question(quiz_number):
    # retrieve the quiz
    quiz = Quiz.objects.filter(id=quiz_number)
    # get related choices
    choices = Choice.objects.filter(quiz__q_order=quiz_number)
    assert len(quiz) == 1
    # get all users id.
    user_ids = [u.user_id for u in User.objects.all()]
    buttons_template = ButtonsTemplate(
        title=f"クイズ {quiz_number}",
        text=quiz[0].quiz_body,
        actions=[
            MessageAction(label=choice.text, text=choice.text) for choice in choices
        ],
    )
    template_message = TemplateSendMessage(
        alt_text=f"クイズ {quiz_number}を出題します！", template=buttons_template
    )
    # 全員に送信
    for user_id in user_ids:
        line_bot_api.push_message(to=user_id, messages=template_message)

# ButtonsTemplate
# https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-kitchensink/app.py#L208
def push_message(request):
    
    if request.method != "POST":
        return HttpResponse("You must use POST method")
    # https://stackoverflow.com/questions/67447272/cannot-parse-formdata-into-django-backend
    quiz_number = request.POST.get("quiz_number", None)
    if quiz_number is None:
        return HttpResponse("You must attach the quiz_number parameter")
    push_question(quiz_number)
    return HttpResponse("good job!")
