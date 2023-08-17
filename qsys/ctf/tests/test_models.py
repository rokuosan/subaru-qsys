from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from app.models.app_user import AppUser
from ctf.models.contest import Contest
from ctf.models.player import Player
from ctf.models.team import Team


class CtfModelTests(TestCase):
    def setUp(self):
        # Create User
        self.user = AppUser.objects.create_user(
            username="Test Tarou",
        )

        # Create Player
        self.player = Player.objects.create(
            name="Test Tarou Player",
            user=self.user,
        )

        # Create Team
        self.team = Team.objects.create(
            name="Test Team",
        )
        self.team.members.add(self.player)

        # Create Contest
        self.contest = Contest.objects.create(
            id="test",
            display_name="Test Contest",
            description="test",
            status=Contest.Status.RUNNING,
            start_at=timezone.now(),
            end_at=timezone.now() + timezone.timedelta(days=1),
        )
        self.contest.teams.add(self.team)

    def test_player(self):
        self.assertEqual(self.player.name, "Test Tarou Player")
        self.assertEqual(self.player.user, self.user)

    def test_team(self):
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.members.first(), self.player)

    def test_contest(self):
        self.assertEqual(self.contest.id, "test")
        self.assertEqual(self.contest.display_name, "Test Contest")
        self.assertEqual(self.contest.description, "test")
        self.assertEqual(self.contest.status, Contest.Status.RUNNING)
        self.assertLessEqual(self.contest.start_at, self.contest.end_at)
        self.assertEqual(self.contest.teams.first(), self.team)

    def test_reverse_reference(self):
        user = AppUser.objects.create(
            username="test_user",
        )
        player = Player.objects.create(
            name="test_player",
            user=user,
        )

        self.assertEqual(player, user.player)

    def test_manager_contest_view_redirect_check(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "ctf:manager_contest", kwargs={"contest_id": self.contest.id}
            )
        )
        self.assertNotEqual(response.status_code, 200)
