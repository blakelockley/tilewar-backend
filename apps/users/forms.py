from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import EmailUser


class EmailUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = EmailUser
        fields = ("email", "first_name", "last_name")


class EmailUserChangeForm(UserChangeForm):
    class Meta:
        model = EmailUser
        fields = ("email", "first_name", "last_name")

