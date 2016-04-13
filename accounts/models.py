from datetime import date

from django.db import models
from django.contrib.auth.models import User

class GoalSetter(models.Model):
    """
    A GoalSetter differs from a User only because it has a running tally of each user's WoohooList points.
    """
    user = models.OneToOneField(User)
    points = models.IntegerField(default=30)

    def __unicode__(self):
        return self.user.username

    def get_current_goal_id(self):
        from goals.models import Goal
        return Goal.objects.get(creator__user__id=self.user.id, completed=False).id

class Friendship(models.Model):
    """
    When a user creates a Friendship object with another user, they can view that person's recently completed
    Steps on their Friends page. The other user would need to create a separate Friendship object to see their
    steps.
    """

    # TODO: Congratulate users on friendiversaries.

    main_user = models.ForeignKey(
        User,
        null=True,
    )
    friend_users = models.ForeignKey(
        User,
        null=True,
        related_name="friends",
    )
    start_date = models.DateField(
        default=date.today
    )