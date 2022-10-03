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

    if request.method == 'POST':
        
        # get X-Line-Signature header value
        import json
        signature = request.headers['X-Line-Signature']
        # body = json.loads(request.body.decode('utf-8'))

        # get request body as text
        body = request.body.decode("utf-8")

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")

    return HttpResponse("Done")


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user = User(user_id=event.source.user_id)
    def extract_answer(message):
        import re
        res = re.findall(string=message, pattern=r"^Q-(\d{1,2}): (\d{1})")
        if (res) != 1:
            # 雑談が挟まれたら、写真などを返す？
            return None, None
        else: 
            q_number, ans = list(map(int, res[0]))
            return q_number, ans
    q_number, ans = extract_answer(event.message.text)
    if q_number is None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ちょっと何言ってるか良くわからない。"))
    else:
        # 問題に対する回答ぽい場合は、答え合わせ処理にすすむ
        t_or_f = check_answer(q_number, ans)
        user.score += t_or_f
        user.save()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="回答有難うございます！"))


def check_answer(q_number, answer):
    """ Questionに対する回答の答え合わせ """
    return 0

# register uuids and names
@handler.add(FollowEvent)
def add_follower(event):
    """ follow eventが発生したタイミングで起動する """

    pdb.set_trace()
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
        to=participant_userId,
        messages=TextSendMessage(text=f"フォロー有難うございます！{name}")
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