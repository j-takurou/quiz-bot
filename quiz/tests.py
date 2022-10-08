from argparse import Action
from unicodedata import name
from django.test import TestCase
from django.test import Client
from django.utils import timezone
import quiz.views as TARGET
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from quiz.models import User, Quiz, Choice

from linebot.models import FollowEvent
import os

# TODO: まず先にpush-msg 関数用のテストを実装する


class TestQuizView(TestCase):
    def setUp(self) -> None:
        self.TEST_USER_LINE_ID = os.environ.get("TEST_USER_LINE_ID")
        User.objects.create(user_id=self.TEST_USER_LINE_ID, name="Jumpei", score=10)
        Quiz.objects.create(
            id=1, q_order=1, quiz_body="「俺じゃなきゃ見逃しちゃうね...」この台詞を放ったキャラクターの名前は？"
        )
        
        Choice.objects.create(text="団長の手刀を見逃さなかった人", is_correct=True, quiz=Quiz(id=1))
        Choice.objects.create(text="サトシ", is_correct=True, quiz=Quiz(id=1))
        Choice.objects.create(text="ゲンゴロウ", is_correct=True, quiz=Quiz(id=1))

        return super().setUp()

    
    def test_push_message(self):
        # User.objects.all = MagicMock(return_value=[User(id=1, user_id=self.TEST_USER_LINE_ID, name="Jumpei")])
        request = Client()
        response = request.post("/push_message/", {"quiz_number": 1})
        self.assertEqual(response.status_code, 200)
    
    @unittest.skip("completed test")
    @patch("quiz.views.line_bot_api.push_message")
    def test_add_follower(self, patch_push_message):
        patch_push_message.return_values = True
        import pdb

        # pdb.set_trace()
        # XXX:
        # line API model Eventをテスト時にどういう風に用意する？

        follow_event = FollowEvent()
        TARGET.add_follower(follow_event)

    def test_push_quiz(self):
        request = Client()
        pass
