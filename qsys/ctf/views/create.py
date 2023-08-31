from django import forms
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from ctf.models.question import Question
from ctf.models.team import Team
from ctf.models.contest import Contest


class _CreateContestForm(forms.Form):
    id = forms.CharField(
        label="コンテストID",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]{4,}$",
                message="半角英数字とアンダースコアのみ使用できます。",
            ),
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "例: contest_2023",
            }
        ),
    )

    name = forms.CharField(
        label="コンテスト名",
        widget=forms.TextInput(
            attrs={
                "placeholder": "例: 2023年度 CTFコンテスト",
            }
        ),
    )

    start_at = forms.SplitDateTimeField(
        widget=AdminSplitDateTime(),
        label="開始日時",
    )
    end_at = forms.SplitDateTimeField(
        widget=AdminSplitDateTime(),
        label="終了日時",
    )

    status = forms.ChoiceField(
        label="コンテストの状態",
        choices=(
            ("preparing", "準備中"),
            ("running", "開催中"),
            ("paused", "一時停止中"),
            ("finished", "終了"),
        ),
        initial="preparing",
    )

    is_open = forms.BooleanField(
        label="コンテストを公開する",
        required=False,
        initial=True,
    )

    teams = forms.MultipleChoiceField(
        label="参加チーム",
        required=False,
    )

    questions = forms.MultipleChoiceField(
        label="問題",
        required=False,
    )

    is_team_ranking_public = forms.BooleanField(
        label="チームランキング(Team Ranking)を公開する",
        required=False,
        initial=True,
    )

    is_player_ranking_public = forms.BooleanField(
        label="プレイヤーランキング(Player Ranking)を公開する",
        required=False,
        initial=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # チームを取得
        teams = []
        for team in Team.objects.all():
            teams.append((team.id, team.name))
        self.fields["teams"].choices = teams

        # 問題を取得
        questions = []
        for question in Question.objects.all():
            questions.append((question.id, question.title))
        self.fields["questions"].choices = questions

    def clean_id(self):
        id = self.cleaned_data["id"]

        # 既にコンテストが存在するかどうか
        if len(Contest.objects.filter(id=id)) > 0:
            raise forms.ValidationError("既にコンテストが存在します。")

        # 予約済みのIDかどうか
        if id in ["create", "admin", "manager"]:
            raise forms.ValidationError("予約済みのIDです。")

        return id

    def clean_teams(self):
        teams = self.cleaned_data["teams"]

        # 同じ人物を含むチームがあるかどうか
        am = []
        for team_id in teams:
            team = Team.objects.get(id=team_id)

            for player in team.members.all():
                if player in am:
                    raise forms.ValidationError(
                        "同じ人物を含むチームがあります。"
                    )
                am.append(player)

        return teams

    def save(self):
        # コンテストを作成
        contest = Contest.objects.create(
            id=self.cleaned_data["id"],
            display_name=self.cleaned_data["name"],
            start_at=self.cleaned_data["start_at"],
            end_at=self.cleaned_data["end_at"],
            status=self.cleaned_data["status"],
            is_open=self.cleaned_data["is_open"],
            is_team_ranking_public=self.cleaned_data[
                "is_team_ranking_public"
            ],
            is_player_ranking_public=self.cleaned_data[
                "is_player_ranking_public"
            ],
        )

        return contest


@login_required
def create_view(request: HttpRequest):
    if not request.user.is_admin:
        messages.error(request, "管理者ではありません。")
        return redirect("ctf/index.html")

    # プレイヤーを取得
    try:
        request.user.player
    except Exception:
        messages.error(request, "プレイヤーデータがありません。")
        return redirect("ctf/index.html")

    ctx = {"form": _CreateContestForm()}

    if request.method == "POST":
        form = _CreateContestForm(request.POST)

        if form.is_valid():
            # コンテストを作成
            contest = form.save()

            # チームを追加
            for team_id in form.cleaned_data["teams"]:
                team = Team.objects.get(id=team_id)
                contest.teams.add(team)

            # 問題を追加
            for question_id in form.cleaned_data["questions"]:
                question = Question.objects.get(id=question_id)
                contest.questions.add(question)

            # メッセージを表示
            messages.success(request, "コンテストを作成しました。")
            return redirect("ctf:home", contest_id=contest.id)
        else:
            messages.error(request, "入力内容に誤りがあります。")
            ctx["form"] = form

    return render(request, "ctf/create.html", ctx)
