from django import forms


class LestaForm(forms.Form):
    file = forms.FileField(label='Файл:', required=False)
