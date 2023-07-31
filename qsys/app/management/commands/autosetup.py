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

    def handle(self, *args, **options):
        data = self.read_yaml()
        if data is None:
            return
        qsys = data["qsys"]

        self.simple_setup(qsys, "difficulty", CtfQuestionDifficulty)
        self.simple_setup(qsys, "category", CtfQuestionCategory)
        self.simple_setup(qsys, "team", CtfTeam)
        self.setup_questions(qsys)

        print("All Setup Completed.")
