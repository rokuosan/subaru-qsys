from django import forms

from ctf.models.contest import Contest


class ScoreSettingForm(forms.Form):
    show_team_rankinng = forms.BooleanField(
        label="チームランキング(Team Ranking)を公開する",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    show_player_ranking = forms.BooleanField(
        label="プレイヤーランキング(Player Ranking)を公開する",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, contest: Contest, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            "show_team_rankinng"
        ].initial = contest.is_team_ranking_public
        self.fields[
            "show_player_ranking"
        ].initial = contest.is_player_ranking_public

    def clean(self):
        cleaned_data = super().clean()
        team = cleaned_data.get("show_team_rankinng")
        player = cleaned_data.get("show_player_ranking")

        if not team and not player:
            raise forms.ValidationError(
                "チームランキングまたはプレイヤーランキングの少なくとも一方を公開する必要があります"
            )

        return cleaned_data

    def save(self):
        pass
