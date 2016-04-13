from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import GoalSetter

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2')

    def save(self):
        new_user = super(NewUserForm, self).save()
        GoalSetter.objects.create(
            user=new_user,
        )
        password = self.cleaned_data['password1']
        new_user.set_password(password)
        new_user.save()
        return new_user
