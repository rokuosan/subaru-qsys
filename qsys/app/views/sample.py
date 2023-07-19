from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render


class SampleFormView(forms.Form):
    text = forms.CharField(
        label="Text", max_length=100, required=True, widget=forms.TextInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        text_element = self.fields["text"]

        text_element.widget.attrs["placeholder"] = "Text"

        text_element.widget.attrs["autocomplete"] = "off"

        text_element.widget.attrs["class"] = "form-control"

    def clean_text(self):
        text = self.cleaned_data["text"]
        if len(text) < 3:
            raise forms.ValidationError("テキストは3文字以上である必要があります。")

        return text

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

        if text is None:
            raise forms.ValidationError("テキストを入力してください。")

        return cleaned_data

    def save(self):
        pass


def sample_view(request):
    form = SampleFormView(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Success {form.cleaned_data['text']}")
            return render(request, "sample.html", {"form": form})

    return render(request, "sample.html", {"form": form})
