import getpass
from django.core.management.base import BaseCommand

from app.models.app_user import AppUser
from ctf.models.player import Player


class Command(BaseCommand):
    help = "管理者ユーザを作成します"

    def handle(self, *args, **options):
        print(self.help)

        username = input("ユーザ名: ")
        password = getpass.getpass("パスワード: ")

        try:
            AppUser.objects.create_superuser(username, password)
            Player.objects.create(
                user=AppUser.objects.get(username=username), name=username
            )
        except Exception as e:
            print("Failed")
            print(e)
            return

        print("Done.")
