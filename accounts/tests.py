from django.test import TestCase
from django import forms
from django.contrib.auth.models import User

from .models import GoalSetter
from .forms import NewUserForm

class TestNewUserForm(TestCase):

    def setUp(self):
        self.data = {
            'username': 'rachel',
            'email': 'info@rachelleahklein.com',
            'password1': 'testytest',
            'password2': 'testytest',
        }

    def test_goalsetter_created_on_save(self):
        self.assertEqual(GoalSetter.objects.count(), 0)
        form = NewUserForm(self.data)
        form.save()

        self.assertEqual(GoalSetter.objects.count(), 1)

    def test_user_created_on_save(self):
        """
        Each instance of GoalSetter should also create an instance of the User class
        that is connected to it.
        """

        self.assertEqual(User.objects.count(), 0)
        form = NewUserForm(self.data)
        form.save()

        self.assertEqual(User.objects.count(), 1)

    def test_points_assigned_at_init(self):
        """
        Each user gets 30 points just for signing up.
        """
        form = NewUserForm(self.data)
        form.save()

        new_goalsetter = GoalSetter.objects.first()

        self.assertEqual(new_goalsetter.points, 30)