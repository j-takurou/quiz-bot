import pdb
from django.http import HttpResponse
import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from quiz.models import User, Quiz

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    TextSendMessage,
    ButtonsTemplate, 
    FollowEvent, 
    TemplateSendMessage,
    MessageAction,
)

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@csrf_exempt
def health_check(request):

    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def callback(request):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# register uuids and names
@handler.add(FollowEvent, message=TextMessage)
def add_follower(event):
    """ follow eventが発生したタイミングで起動する """
    # クイズをPUSH送信するためにuuidsを保存
    participant_userId = event.source.userId
    # extract user name from user profile

    try:
        profile = line_bot_api.get_profile(participant_userId)
        name = profile.displayName
    except LineBotApiError as e:
        # エラーハンドリング
        pass
    # save users
    User(user_id=participant_userId, name=name).save()

    # フォロー有難う！とメッセージを返す
    line_bot_api.push_message(
        to=participant_userId,
        messages=f"フォロー有難うございます！{name}"
        )




# ButtonsTemplate
# https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-kitchensink/app.py#L208
def push_message(request):
    
    if request.method != "POST":
        return HttpResponse("You must use POST method")
    
    # https://stackoverflow.com/questions/67447272/cannot-parse-formdata-into-django-backend
    quiz_number = request.POST.get("quiz_number", None)
    if quiz_number is None:
        return HttpResponse("You must attach the quiz_number parameter")

    # retrieve the quiz
    quiz = Quiz(id=quiz_number)
    
    # get all users id.
    user_ids = [u.user_id for u in User.objects.all()]

    buttons_template = ButtonsTemplate(
                title='DUSTクイズ！', text='篠田が酔っ払ったときに放った名言は？', actions=[
                    MessageAction(label='人間ていいな', text='人間ていいな'),
                    MessageAction(label='人間てのは酒を飲むんよ', text='酒のもう？'),
                    MessageAction(label='ピィぃ', text='ピィぃぃlいいいいいいいいいいいいいいいいいいい')
                ])

    template_message = TemplateSendMessage(
        alt_text='Buttons alt text', template=buttons_template)

    # line_bot_api.reply_message(event.reply_token, template_message)    
    # 全員に一斉送信できるようなmethodはないか？
    for user_id in user_ids:
        line_bot_api.push_message(
            to=user_id,
            messages=template_message
        )
#  
    return HttpResponse("good job!")