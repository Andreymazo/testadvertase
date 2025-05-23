from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from pip._internal.utils._jaraco_text import _
from django.contrib import messages
from django.core.exceptions import ValidationError

class MyAuthForm(AuthenticationForm):
    # Сейчас из темплейта сообщения
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }


""""Здесь наверное лучше валидацию делать, хотя не проходят без ревеста мессаджиз,\
      а как в форму реквест подать не знаю, в сериализаторе можно, а в форме фроде нет"""
class MyRegForm(forms.Form):
    password1 = forms.CharField(max_length=150, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=150, widget=forms.PasswordInput())
    email = forms.EmailField()
    def clean(self):
        if not self.cleaned_data['password1'] == self.cleaned_data['password2']:
                raise ValidationError("Passwords are not equals")
        return super().clean()

