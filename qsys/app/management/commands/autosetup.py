import random
from django.core.management.base import BaseCommand
import yaml

from app.models.difficulty import CtfQuestionDifficulty
from app.models.category import CtfQuestionCategory
from app.models.team import CtfTeam
from app.models.question import CtfQuestion
from app.models.app_user import AppUser


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
        for question in questions:
            try:
                title = question["title"]
                print(f"- {title}", end=" ")

                ql = CtfQuestion.objects.filter(title=title)
                if ql.exists():
                    print("Already exists")
                    continue

                random = AppUser.objects.make_random_password()

                cat_name = question["category"]
                dif_name = question["difficulty"]
                category = CtfQuestionCategory.objects.get(name=cat_name)
                difficulty = CtfQuestionDifficulty.objects.get(name=dif_name)
                flag = question.get("flag", f"flag{{{random}}}")
                content = question.get("content", title)
                point = question.get("point", 0)
                explanation = question.get("explanation", None)
                file_path = question.get("file_path", None)
                is_published = question.get("is_published", True)
                is_practice = question.get("is_practice", False)
                note = question.get("note", None)

                CtfQuestion(
                    category=category,
                    title=title,
                    content=content,
                    explanation=explanation,
                    point=point,
                    flag=flag,
                    difficulty=difficulty,
                    file_path=file_path,
                    is_published=is_published,
                    is_practice=is_practice,
                    note=note,
                ).save()

                print("OK")
            except (KeyError, TypeError) as e:
                print("Failed")
                print("\nCouldn't get value {}".format(e))
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

                    # Team
                    team = user.get("team", None)
                    if team is not None:
                        try:
                            team = CtfTeam.objects.get(name=team)
                        except CtfTeam.DoesNotExist:
                            print("Team not found")
                            continue

                    # Flags
                    is_admin = user.get("is_admin", False)
                    is_staff = user.get("is_staff", False)
                    is_superuser = user.get("is_superuser", False)
                    is_active = user.get("is_active", True)

                    # Create
                    u = AppUser(
                        username=user["username"],
                        team=team,
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
        csv = "\n".join([f"{u}, {p}" for u, p in pw_list])
        rand = random.randrange(1000, 10000)
        with open(f"passwords_{rand}.csv", "w") as f:
            f.write(csv)

        print("Users Done.")
        print()

    def handle(self, *args, **options):
        data = self.read_yaml()
        if data is None:
            return
        qsys = data["qsys"]

        self.simple_setup(qsys, "difficulty", CtfQuestionDifficulty)
        self.simple_setup(qsys, "category", CtfQuestionCategory)
        self.simple_setup(qsys, "team", CtfTeam)
        self.setup_questions(qsys)
        self.setup_users(qsys)

        print("All Setup Completed.")
