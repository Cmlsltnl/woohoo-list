from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.middleware import csrf as ajax_csrf

from .models import Goal, Step, StepComment
from .forms import GoalSettingForm, StepCreationForm, CommentForm

from accounts.models import GoalSetter

@login_required
def step_detail_page(request, goal_id, step_id):
    """
    On the step detail page, users can leave comments on their friends' completed steps.
    """

    user_id = request.user.id
    step = Step.objects.get(id=step_id)
    goal = Goal.objects.get(id=goal_id)
    profile_user = User.objects.get(goalsetter__goal__id=goal_id)
    comments = StepComment.objects.filter(comment_step__id=step_id)

    # My_profile variable is set because users who are viewing their own steps do not get the option
    # to comment.
    my_profile = False
    if user_id == profile_user.id:
        my_profile = True
    user = GoalSetter.objects.get(user__id=user_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(step_id, user_id)
            return HttpResponseRedirect(reverse('step_detail_page', args=[goal_id, step_id]))
    else:
            form = CommentForm()
    context = {
        'user': user,
        'profile_user': profile_user,
        'form': form,
        'goal': goal,
        'step': step,
        'my_profile': my_profile,
        'comments': comments,
    }

    context.update(csrf(request))

    return render_to_response(
        'step_detail_page.html',
        context=context,
    )

@login_required
def goal_detail_page(request, goal_id=None):
    """
    Users can see their own and others' goals complete with all the steps.
    """
    # TODO: Display percent completion with a chart or graph.
    user_id = request.user.id
    profile_user = User.objects.get(goalsetter__goal__id=goal_id)
    my_profile = False
    if user_id == profile_user.id:
        my_profile = True
    user = GoalSetter.objects.get(user__id=user_id)
    steps = Step.objects.filter(parent_goal__id=goal_id)
    incomplete_steps = steps.exclude(completed=True)

    context = {
        'user': user,
        'goal': Goal.objects.get(id=goal_id),
        'form': GoalSettingForm,
        'steps': steps,
        'incomplete_steps': incomplete_steps,
        'goal_id': goal_id,
        'my_profile': my_profile,
        'profile_user': profile_user,
        'csrf_token': ajax_csrf.get_token(request),
    }

    context.update(csrf(request))

    return render_to_response(
        'goal_detail_page.html',
        context=context,
    )

@login_required
def goal_setting_page(request, username):
    user_id = request.user.id
    user = GoalSetter.objects.get(user__username=username)
    if request.method == 'POST':
        form = GoalSettingForm(request.POST, user_id=user_id)
        if form.is_valid():
            goal = form.save()
            return HttpResponseRedirect(reverse('step_creation_page', args=[goal.id]))
    else:
            form = GoalSettingForm(user_id=user_id)

    context = {
        'user': user,
        'form': form.as_p(),
    }

    context.update(csrf(request))

    return render_to_response(
        'goal_setting_page.html',
        context=context,
    )

@login_required
def step_creation_page(request, goal_id):
    """
    After visiting the goal setting page, the step creation page allows the user to create all the
    steps in their new goal.
    """
    user_id = request.user.id
    user = GoalSetter.objects.get(user__id=user_id)

    steps = Step.objects.filter(parent_goal__id=goal_id)

    if request.method == 'POST':
        form = StepCreationForm(request.POST)
        if form.is_valid():
            step = form.save(goal_id)
            return HttpResponseRedirect(reverse('step_creation_page', args=[goal_id]))
            # TODO: Make a fancier page that rewards the user with their first points!
    else:
            form = StepCreationForm()

    context = {
        'user': user,
        'form': form.as_p(),
        'steps': steps,
        'goal_id': goal_id,
    }

    context.update(csrf(request))

    return render_to_response(
        'step_creation_page.html',
        context=context,
    )

@login_required
def edit_goal(request, goal_id):
    user_id = request.user.id
    user = GoalSetter.objects.get(user__id=user_id)

    goal = get_object_or_404(Goal, id=goal_id)
    user_id = request.user.id

    if request.method == 'POST':
        form = GoalSettingForm(request.POST, instance=goal, user_id=user_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('goal_detail_page', args=[goal_id]))

    else:
        form = GoalSettingForm(instance=goal, user_id=user_id)

    return render(
        request,
        'edit_goal.html',
        context={
            'user': user,
            'form': form.as_p,
        }
    )
@login_required
def step_completion(request):
    """
    This view exists only to deal with the Ajax through which step completion works.
    """
    if request.method == 'POST':
        step_id = request.POST['step_id']
        try:
            step = Step.objects.get(pk=step_id)
        except DoesNotExist:
            return JsonResponse({"result": False, "error": "Step does not exist"})

        # Set step as completed
        step.completed = True

        # Mark date and time step is completed
        step.completed_date = datetime.now()
        step.save()

        # Augment total points for goal setter
        goalsetter = GoalSetter.objects.get(user=request.user)
        goalsetter.points += 10
        goalsetter.save()

        # Changing goal to completed if all steps are completed

        completed = False
        user = GoalSetter.objects.get(user__id=request.user.id)
        all_goals = user.goal_set.all()
        goal = all_goals.get(completed=False)
        if goal.all_steps_completed():
            goal.completed = True
            goal.save()
            goalsetter.points += 50
            goalsetter.save()
            completed = True

        return JsonResponse({"result": True, "current_points": goalsetter.points, "completed": completed})
