import datetime
import hashlib
import uuid
import os
import shutil
from django.core.management.base import BaseCommand
import yaml

from app.models.app_user import AppUser
from ctf.models.player import Player
from ctf.models.team import Team
from ctf.models.question import Question, Category, Difficulty


class Command(BaseCommand):
    help = "init.yamlに定義した内容をもとに、Q-Sysのセットアップを行います。"

    def read_yaml(self) -> dict:
        print(self.help)

        text = None
        try:
            with open("init.yaml", "r") as f:
                text = f.read()
        except FileNotFoundError:
            print("init.yaml not found")
            return None

        if text is None:
            print("init.yaml is empty")
            return None

        data = None
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            print("init.yaml is not valid YAML")

        return data

    def simple_setup(self, yml: dict, key: str, model):
        print(f"Setting up {key}...")
        data = yml[key]
        for item in data:
            print(f"- {item}", end=" ")
            try:
                i = model.objects.filter(name=item)
                if i.exists():
                    print("Already exists")
                    continue
                d = model(name=item)
                d.save()
                print("OK")
            except Exception as e:
                print("Failed")
                print(e)
                return
        print(f"{key} Done.")
        print()

    def setup_questions(self, yml: dict):
        print("Setting up Questions...")
        questions = yml["question"]
        for q in questions:
            print(f"- {q['title']}", end=" ")
            try:
                title = q["title"]
                description = q["description"]
                flag = q["flag"]
                point = q["point"]
                category = Category.objects.get(name=q["category"])
                difficulty = Difficulty.objects.get(name=q["difficulty"])
                is_open = q.get("is_open", True)
                if Question.objects.filter(title=title).exists():
                    print("Already exists")
                    continue
                qdata = Question(
                    title=title,
                    description=description,
                    flag=flag,
                    point=point,
                    category=category,
                    difficulty=difficulty,
                    is_open=is_open,
                )
                qdata.save()

                filepath = q.get("file", None)
                if filepath is not None:
                    # ファイルの存在確認
                    is_file = os.path.isfile(filepath)
                    if not is_file:
                        print("File not found")
                        continue
                    # ディレクトリの作成
                    qid = qdata.id
                    qdir = f"./static/questions/{qid}/"
                    os.makedirs(qdir, exist_ok=True)
                    # ファイルのコピー
                    shutil.copy(filepath, qdir)

                    qdata.file_path = (
                        f"static/questions/{qid}/{os.path.basename(filepath)}"
                    )
                    qdata.save()

                print("OK")
            except Exception as e:
                print("Failed")
                print(e)
                return
        print("Questions Done.")
        print()

    def setup_users(self, yml: dict):
        data = yml["user"]
        pw_list = []

        roughed = data.get("roughed", None)
        if roughed is not None and type(roughed) is list:
            print("Setting up Roughed Users...")
            for username in roughed:
                print(f"- {username}", end=" ")
                try:
                    u = AppUser.objects.filter(username=username)
                    if u.exists():
                        print("Already exists")
                        continue
                    pw = AppUser.objects.make_random_password()
                    pw_list.append((username, pw))
                    u = AppUser(username=username)
                    u.set_password(pw)
                    u.save()
                    print("OK")
                except Exception as e:
                    print("Failed")
                    print(e)
                    return

        detailed = data.get("detailed", None)
        if detailed is not None and type(detailed) is list:
            print("Setting up Detailed Users...")
            for user in detailed:
                print(f"- {user['username']}", end=" ")
                try:
                    # Check
                    u = AppUser.objects.filter(username=user["username"])
                    if u.exists():
                        print("Already exists")
                        continue

                    # Password
                    pw = user.get("password", None)

                    # Flags
                    is_admin = user.get("is_admin", False)
                    is_staff = user.get("is_staff", False)
                    is_superuser = user.get("is_superuser", False)
                    is_active = user.get("is_active", True)

                    # Create
                    u = AppUser(
                        username=user["username"],
                        # team=team,
                        is_admin=is_admin,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        is_active=is_active,
                    )

                    if pw is not None:
                        u.set_password(pw)
                    else:
                        pw = AppUser.objects.make_random_password()
                        pw_list.append((user["username"], pw))
                        u.set_password(pw)
                    u.save()
                    print("OK")
                except Exception as e:
                    print("Failed")
                    print(e)
                    return

        # Print password list as csv
        if len(pw_list) > 0:
            csv = "\n".join([f"{u}, {p}" for u, p in pw_list])
            uid = uuid.uuid4()
            today = datetime.date.today()
            hash = hashlib.sha256(f"{uid}{today}".encode()).hexdigest()
            with open(f"passwords_{hash}.csv", "w") as f:
                f.write(csv)

        print("Users Done.")
        print()

    def setup_player(self, yml: dict):
        print("Setting up Players...")
        data = yml["player"]
        for player in data:
            print(f"- {player}", end=" ")
            try:
                username = player
                u = AppUser.objects.get(username=username)
                if Player.get_player(u) is not None:
                    print("Already exists")
                    continue
                p = Player.objects.create(name=username, user=u)
                p.save()
                print("OK")
            except Exception as e:
                print("Failed")
                print(e)
                return
        print("Players Done.")
        print()

    def handle(self, *args, **options):
        data = self.read_yaml()
        if data is None:
            return
        qsys = data["qsys"]

        self.simple_setup(qsys, "difficulty", Difficulty)
        self.simple_setup(qsys, "category", Category)
        self.simple_setup(qsys, "team", Team)
        self.setup_questions(qsys)
        self.setup_users(qsys)
        self.setup_player(qsys)

        print("All Setup Completed.")
