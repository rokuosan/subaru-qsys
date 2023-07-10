from django import forms
from app.models.app_user import AppUser


class CreateUserForm(forms.Form):
    name = forms.CharField(
        label="Username", max_length=100, required=True, widget=forms.TextInput
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        required=True,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name_element = self.fields["name"]
        password_element = self.fields["password"]

        name_element.widget.attrs["placeholder"] = "Taro Yamada"
        password_element.widget.attrs["placeholder"] = "********"

        name_element.widget.attrs["autocomplete"] = "off"
        password_element.widget.attrs["autocomplete"] = "new-password"

        name_element.widget.attrs["class"] = "form-control"
        password_element.widget.attrs["class"] = "form-control"

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise forms.ValidationError("ユーザー名は3文字以上である必要があります。")

        return name

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 3:
            raise forms.ValidationError("パスワードは3文字以上である必要があります。")

        return password

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")

        if name is None or password is None:
            raise forms.ValidationError("ユーザー名とパスワードを入力してください。")

        if name:
            if AppUser.objects.filter(username=name).exists():
                raise forms.ValidationError("そのユーザー名は既に使われています。")

        return cleaned_data

    def save(self):
        user = AppUser.objects.create_user(
            self.cleaned_data["name"], self.cleaned_data["password"]
        )
        return user
