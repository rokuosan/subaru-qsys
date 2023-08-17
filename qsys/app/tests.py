from django.test import TestCase
from django.utils import timezone

from ctf.models.question import Category, Difficulty, Question
from ctf.models.player import Player
from ctf.models.team import Team
from app.models.app_user import AppUser
from ctf.models.contest import Contest


class ViewTests(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            username="test user",
        )
        self.player = Player.objects.create(
            name="test player",
            user=self.user,
        )
        self.team = Team.objects.create(
            name="test team",
        )
        self.team.members.add(self.player)

        self.contest = Contest.objects.create(
            id="test_contest",
            description="test contest",
            status=Contest.Status.RUNNING,
            start_at=timezone.now(),
            end_at=timezone.now() + timezone.timedelta(days=1),
        )
        self.contest.teams.add(self.team)

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_question_detail(self):
        d = Difficulty.objects.create(name="Easy")
        c = Category.objects.create(name="test")

        question = Question.objects.create(
            title="問題1",
            flag="flag{test}",
            point=100,
            category=c,
            difficulty=d,
            is_open=True,
        )

        self.contest.questions.add(question)

        self.client.force_login(self.user)
        response = self.client.get(f"/questions/{question.id}/")
        self.assertEqual(response.status_code, 200)
