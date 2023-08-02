from django.utils import timezone
from django.test import TestCase

from app.models.app_user import AppUser
from ctf.models.contest import Contest
from ctf.models.player import Player
from ctf.models.team import Team


class CtfModelTests(TestCase):
    def test_start_at(self):
        time = timezone.now()
        ctf = Contest.objects.create(
            id="test",
        )
        self.assertLessEqual(time, ctf.start_at)

    def test_end_at(self):
        ctf = Contest.objects.create(
            id="test",
        )
        self.assertLessEqual(ctf.start_at, ctf.end_at)

    def test_reverse_reference(self):
        user = AppUser.objects.create(
            username="test_user",
        )
        player = Player.objects.create(
            name="test_player",
            user=user,
        )
        user1 = AppUser.objects.create(
            username="test_user1",
        )

        self.assertEqual(player, user.player)
        self.assertEqual(user1.player, None)
