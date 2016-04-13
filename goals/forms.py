from django.forms import ModelForm, HiddenInput

from .models import Goal, Step, StepComment
from accounts.models import GoalSetter

class GoalSettingForm(ModelForm):
    class Meta:
        model = Goal
        fields = ('creator', 'title', 'description', 'completion_date', 'category')
        # TODO: See if we can add a calendar widget for completion_date

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super(GoalSettingForm, self).__init__(*args, **kwargs)
        self.fields['creator'].initial = GoalSetter.objects.get(user__id=user_id)
        self.fields['creator'].widget = HiddenInput()

class StepCreationForm(ModelForm):
    class Meta:
        model = Step
        fields = ('detail', 'target_date')
        # TODO: Figure out how we could easily duplicate a bunch of steps that are all the same.

    def save(self, goal_id):
        steps = Step.objects.filter(parent_goal__id=goal_id)

        # Assigns a step number relative to all other steps in this goal (for easy display)
        if steps.exists():
            ordered_steps = steps.order_by('step_number')
            step_number = list(ordered_steps.values_list('step_number', flat=True))[-1]+1
        else:
            step_number = 1

        new_step = super(StepCreationForm, self).save()
        new_step.parent_goal_id = goal_id
        new_step.step_number = step_number
        new_step.save()
        return new_step

class CommentForm(ModelForm):
    class Meta:
        model = StepComment
        fields = ('content', )

    def save(self, step_id, user_id):

        new_comment = super(CommentForm, self).save()

        author = GoalSetter.objects.get(user__id=user_id)

        new_comment.author = author
        new_comment.comment_step_id = step_id

        new_comment.save()

        # People who leave comments on other people's accomplishments get points too!
        author.points += 8
        author.save()

        return new_comment
