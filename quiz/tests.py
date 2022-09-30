from django.test import TestCase
from django.test import Client
from django.utils import timezone
import quiz.views as TARGET
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from quiz.models import User, Quiz

from linebot.models import FollowEvent
import os

# TODO: まず先にpush-msg 関数用のテストを実装する

class TestQuizView(TestCase):

    def setUp(self) -> None:
        self.TEST_USER_LINE_ID = os.environ.get("TEST_USER_LINE_ID")
        return super().setUp()

    @unittest.skip("skip at add-follow-event branch")
    @patch("quiz.models.User.objects.all")
    @patch("quiz.models.Quiz")
    def test_push_message(self, patch_Users, patch_Quiz):
        patch_Quiz.return_values = Quiz(q_order=1, quiz_body="ようこそ")
        User.objects.all = MagicMock(return_value=[User(id=1, user_id=self.TEST_USER_LINE_ID, name="Jumpei")])
        request = Client()
        response = request.post('/quiz/push_message/', {'quiz_number':1})
        self.assertEqual(response.status_code, 200)
    
    @patch("quiz.views.line_bot_api.push_message")
    def test_add_follower(self, patch_push_message):
        patch_push_message.return_values = True
        import pdb; pdb.set_trace()
        # XXX:
        # line API model Eventをテスト時にどういう風に用意する？

        follow_event = FollowEvent()
        TARGET.add_follower(follow_event)

