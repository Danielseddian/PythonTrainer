from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class ResolveForm(forms.Form):
    resolve = forms.CharField(max_length=5000, required=True, widget=forms.Textarea)


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")
