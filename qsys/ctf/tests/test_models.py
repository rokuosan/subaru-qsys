from django.utils import timezone
from django.test import TestCase

from qsys.ctf.models.contenst import Contest


class CtfModelTests(TestCase):
    def test_start_at(self):
        time = timezone.now()
        ctf = Contest.objects.create(
            name="test",
        )
        self.assertLessEqual(time, ctf.start_at)

    def test_end_at(self):
        ctf = Contest.objects.create(
            name="test",
        )
        self.assertLessEqual(ctf.start_at, ctf.end_at)
