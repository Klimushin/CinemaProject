from django.contrib.auth.forms import UserCreationForm

from user.models import Customer


class SignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = [
            'username',
            'password1',
            'password2',
        ]
