from django.utils import timezone
from django.test import TestCase

from ctf.models.ctf import CTF


class CtfModelTests(TestCase):
    def test_start_at(self):
        time = timezone.now()
        ctf = CTF.objects.create(
            name="test",
        )
        self.assertLessEqual(time, ctf.start_at)

    def test_end_at(self):
        ctf = CTF.objects.create(
            name="test",
        )
        print(ctf.start_at, ctf.end_at)
        self.assertLessEqual(ctf.start_at, ctf.end_at)

    def test_status(self):
        ctf = CTF.objects.create(
            name="test",
        )
        ctf.set_status(CTF.Status.RUNNING)
        self.assertEqual(ctf.status, CTF.Status.RUNNING)