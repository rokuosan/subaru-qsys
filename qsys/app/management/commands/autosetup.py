import datetime
import hashlib
import uuid
import os
import shutil
from django.core.management.base import BaseCommand
from django.utils import timezone
import yaml

from app.models.app_user import AppUser
from ctf.models.player import Player
from ctf.models.team import Team
from ctf.models.question import Question, Category, Difficulty
from ctf.models.contest import Contest


class Command(BaseCommand):
    help = "init.yamlに定義した内容をもとに、Q-Sysのセットアップを行います。"

    def read_yaml(self) -> dict:
        """init.yamlを読み込みます。

        Returns:
            dict: init.yamlの内容
        """
        print(self.help)

        text = None
        try:
            if os.name == "nt":
                with open("init.yaml", "r", encoding="utf-8_sig") as f:
                    text = f.read()
            else:
                with open("init.yaml", "r", encoding="utf-8") as f:
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
        """名前のみのモデルをセットアップします。

        Args:
            yml (dict): YAMLオブジェクト
            key (str): レコードのキー
            model (_type_): モデル
        """
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
        """問題をセットアップします。

        Args:
            yml (dict): YAMLオブジェクト
        """
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
        """ユーザーをセットアップします。

        Args:
            yml (dict): YAMLオブジェクト
        """
        data = yml["user"]
        pw_list = []

        # Roughed Users
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

        # Detailed Users
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

        # CSVファイルを出力
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
        """プレイヤーをセットアップします。

        Args:
            yml (dict): YAMLオブジェクト
        """
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

    def setup_contest(self, yml: dict):
        """コンテストをセットアップします。

        Args:
            yml (dict): YAMLオブジェクト
        """
        print("Setting up Contest...")
        data = yml["contest"]
        for contest in data:
            cid = contest.get("id", None)
            if cid is None:
                print("Contest ID is not defined")
                continue
            print(f"- {cid}", end=" ")

            if Contest.objects.filter(id=cid).exists():
                print("Already exists")
                continue

            dname = contest.get("display_name", None)
            desc = contest.get("description", "")
            start = contest.get("start_at", None)
            end = contest.get("end_at", None)
            status = contest.get("status", "preparing")
            questions = contest.get("questions", None)
            teams = contest.get("teams", None)
            is_open = contest.get("is_open", True)
            team_rank = contest.get("is_team_ranking_public", True)
            player_rank = contest.get("is_player_ranking_public", False)

            try:
                is_naive_start = True
                is_naive_end = True
                if start is None:
                    start = timezone.now()
                    is_naive_start = False
                if end is None:
                    end = timezone.now() + datetime.timedelta(hours=1)
                    is_naive_end = False
                if type(start) is str:
                    start = datetime.datetime.strptime(
                        start, "%Y-%m-%d %H:%M:%S"
                    )
                if type(end) is str:
                    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                if is_naive_start:
                    start = timezone.make_aware(start)
                if is_naive_end:
                    end = timezone.make_aware(end)
            except Exception as e:
                print("Failed")
                print(e)
                continue

            if status not in ["running", "paused", "finished", "preparing"]:
                print("Unknown status")
                continue

            try:
                c = Contest.objects.create(
                    id=cid,
                    display_name=dname,
                    description=desc,
                    start_at=start,
                    end_at=end,
                    status=status,
                    is_open=is_open,
                    is_team_ranking_public=team_rank,
                    is_player_ranking_public=player_rank,
                )
                c.save()
            except Exception as e:
                print("Failed")
                print(e)
                continue

            if questions is not None:
                for q in questions:
                    try:
                        qdata = Question.objects.get(title=q)
                        c.questions.add(qdata)
                    except Exception:
                        print("No such question: ", q)
                        continue

            if teams is not None:
                for t in teams:
                    try:
                        tdata = Team.objects.get(name=t)
                        c.teams.add(tdata)
                    except Exception:
                        print("No such team: ", t)
                        continue

            print("OK")

        print("Contest Done.")
        print()

    def setup_team(self, yml: dict):
        """チームをセットアップします。

        Args:
            yml (dict): YAMLオブジェクト
        """
        print("Setting up Teams...")
        data = yml["team"]
        for team in data:
            if type(team) is dict:
                name = team.get("name", None)
                if name is None:
                    print("Team name is not defined")
                    continue
                print(f"- {name}", end=" ")

                try:
                    t = Team.objects.filter(name=name)
                    if t.exists():
                        print("Already exists")
                        continue
                    t = Team(name=name)
                    t.save()
                    players = team.get("players", None)
                    if players is None:
                        print("OK")
                        continue
                    for p in players:
                        try:
                            pdata = Player.objects.get(name=p)
                            t.members.add(pdata)
                        except Exception:
                            print("No such player: ", p)
                            continue
                    print("OK")

                except Exception as e:
                    print("Failed")
                    print(e)
                    continue

            else:
                print(f"- {team}", end=" ")
                try:
                    t = Team.objects.filter(name=team)
                    if t.exists():
                        print("Already exists")
                        continue
                    t = Team(name=team)
                    t.save()
                    print("OK")
                except Exception as e:
                    print("Failed")
                    print(e)
                    continue
        print("Teams Done.")
        print()

    def handle(self, *args, **options):
        data = self.read_yaml()
        if data is None:
            return
        qsys = data["qsys"]

        self.simple_setup(qsys, "difficulty", Difficulty)
        self.simple_setup(qsys, "category", Category)
        self.setup_users(qsys)
        self.setup_player(qsys)
        self.setup_team(qsys)
        self.setup_questions(qsys)
        self.setup_contest(qsys)

        print("All Setup Completed.")
