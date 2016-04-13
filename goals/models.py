from django.db import models
from datetime import date
from accounts.models import GoalSetter

class Goal(models.Model):
    """
    Each user has one Goal object at a time. They set a target completion date and choose a category
    (which will be used to search for users with similar goals).
    """
    GOAL_CATEGORIES = (
        ('FIN', 'Finance'),
        ('FIT', 'Fitness'),
        ('LEA', 'Learning'),
        ('PER', 'Personal'),
    )
    creator = models.ForeignKey(
        GoalSetter,
        null=True,
    )
    title = models.CharField(
        max_length=256,
    )
    description = models.TextField()

    completion_date = models.DateField(
        default=date.today,
    )
    category = models.CharField(
        max_length=3,
        choices=GOAL_CATEGORIES,
        null=True,
    )
    completed = models.BooleanField(
        default=False,
    )

    def __unicode__(self):
        return self.title

    def all_steps_completed(self):
        all_steps_completed = False
        completed_steps = 0
        all_steps = self.steps.all()
        for step in all_steps:
            if step.completed:
                completed_steps += 1
        if completed_steps == all_steps.count():
            all_steps_completed = True
        return all_steps_completed

class Step(models.Model):
    """
    Each goal has different steps which the user can customize with a description and target
    completion date. Step numbers are also added so users can keep track of and rearrange the order
    of steps (rearrangement feature will appear in a future version).
    """
    parent_goal = models.ForeignKey(
        Goal,
        related_name="steps",
        null=True,
        blank=True,
    )
    detail = models.CharField(
        max_length=256,
        default="Take one step closer!"
    )
    target_date = models.DateField(
        default=date.today,  # The ideal completion date chosen when step is created.
    )
    completed = models.BooleanField(
        default=False,
    )
    completed_date = models.DateTimeField(
        null=True,
    )  # The actual date step was completed.
    step_number = models.IntegerField(
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.detail

class StepComment(models.Model):
    """
    Users/goal setters can comment on other people's completed steps.
    """
    author = models.ForeignKey(
        GoalSetter,
        null=True,
        blank=False,
    )
    content = models.TextField(
        null=True,
        blank=False
    )
    comment_date = models.DateTimeField(
        auto_now_add=True,
    )
    comment_step = models.ForeignKey(
        Step,
        related_name='comments',
        null=True,
        blank=False
    )
    def __unicode__(self):
        return 'Comment from {} on {}'.format(self.author, self.comment_date)
