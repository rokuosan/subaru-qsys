from django import forms

from app.models.ctf_information import CtfInformation


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

    def __init__(self, ctf: CtfInformation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["show_team_rankinng"].initial = ctf.show_team_ranking
        self.fields["show_player_ranking"].initial = ctf.show_player_ranking

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
