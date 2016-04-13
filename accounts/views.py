from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.middleware import csrf as ajax_csrf

from .models import GoalSetter, Friendship
from goals.models import Goal, Step
from .forms import NewUserForm

@login_required
def profile_page(request, username):

    user_id = request.user.id
    profile_user = User.objects.get(username=username)

    # The same profile template is used whether you are viewing your own profile or someone else's.
    # The my_profile variable tells the template which content to display.
    my_profile = False
    if user_id == profile_user.id:
        my_profile = True

    user = GoalSetter.objects.get(user__id=user_id)

    # The page will also display different content based on whether the user whose profile we're looking
    # at has a current goal or not.
    # TODO: See if the following code can be made DRYer.
    if my_profile:
        if Goal.objects.filter(creator__user__id=user_id, completed=False).exists():
            current_goal = Goal.objects.get(creator__user__id=user_id, completed=False)
            goal_category = current_goal.category
            similar_goals = Goal.objects.filter(category=goal_category, completed=False)
            similar_goals = similar_goals.exclude(creator__user__id=user_id)
        else:
            current_goal = False
            similar_goals = False
    else:
        if Goal.objects.filter(creator__user__id=profile_user.id, completed=False).exists():
            current_goal = Goal.objects.get(creator__user__id=profile_user.id, completed=False)
            goal_category = current_goal.category
            similar_goals = Goal.objects.filter(category=goal_category, completed=False)
            similar_goals = similar_goals.exclude(creator__user__id=user_id)
        else:
            current_goal = False
            similar_goals = False

    # If the user is not viewing their own profile, the friend_profile variable tells the template
    # to display a "friend" or "unfriend" button.
    friend_profile = False
    if not my_profile:
        if Friendship.objects.filter(main_user=user.user, friend_users=profile_user).exists():
            friend_profile = True

    past_goals = Goal.objects.filter(creator__user__id=user_id, completed=True)

    # The profile user (like the user, above) must be passed in as a GoalSetter object so we
    # can display their points.
    profile_user = GoalSetter.objects.get(user__username=username)

    return render_to_response(
        'profile_page.html',
        context={
            'user_id': user_id,
            'user': user,
            'past_goals': past_goals,
            'current_goal': current_goal,
            'similar_goals': similar_goals,
            'my_profile': my_profile,
            'profile_user': profile_user,
            'friend_profile': friend_profile,
            'csrf_token': ajax_csrf.get_token(request),
        }
    )

def new_user_page(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('thank_you', args=[new_user.username]))
    else:
        form = NewUserForm()

    context = {
        'form': form.as_p,
   }
    context.update(csrf(request))

    return render_to_response(
        'new_user_page.html',
        context=context,
    )

@login_required
def thank_you(request, username):
    user = GoalSetter.objects.get(user__username=username)
    return render_to_response(
        'thank_you.html',
        context = {
            'user': user,
        }
    )

def home(request):
    if request.user.id:
        user_id = request.user.id
        user = GoalSetter.objects.get(user__id=user_id)
        context = {
            'user': user,
        }
    else:
        context = {}
    return render_to_response(
        'home.html',
        context=context,
    )

def about(request):
    if request.user.id:
        user_id = request.user.id
        user = GoalSetter.objects.get(user__id=user_id)
        context = {
            'user': user,
        }
    else:
        context = {}
    return render_to_response(
        'about.html',
        context=context,
    )

@login_required
def friends_page(request):
    user = request.user  # For querying purposes only
    goalsetter = GoalSetter.objects.get(user=user)  # For passing in as context (to show user points)

    # Creates a view model for each friend with all the info needed to display their most recent step.
    user_friendships = Friendship.objects.filter(main_user=user)
    user_friends = []
    for friendship in user_friendships:
        user = friendship.friend_users
        user_friends.append(user)
    friend_posts = []
    for friend in user_friends:
        friend_user = friend
        friend_goalsetter = GoalSetter.objects.get(user=friend_user)
        goal = Goal.objects.get(creator=friend_goalsetter, completed=False)
        goal_id = goal.id
        all_steps = Step.objects.filter(parent_goal=goal_id)
        completed_steps = Step.objects.filter(parent_goal=goal, completed=True).order_by('completed_date')
        step_count = all_steps.count()
        completed_step_count = completed_steps.count()
        latest_step = completed_steps.last()
        percent_done = int((completed_step_count/step_count)*100)
        data = {
            'friend_user': friend_user,
            'goal': goal,
            'latest_step': latest_step,
            'percent_done': percent_done,
        }
        friend_posts.append(data)
    context = {
        'user': goalsetter,
        'friend_posts': friend_posts,
    }
    return render_to_response(
        'friends_page.html',
        context=context,
    )

@login_required
def friend_someone(request):
    if request.method == 'POST':
        friend_id = request.POST['user_id']
        action = request.POST['action']

        friend = User.objects.get(id=friend_id)
        user_id = request.user.id
        current_user = User.objects.get(id=user_id)

        # Create new friendship :D
        if action == 'add':
            Friendship.objects.get_or_create(main_user=current_user, friend_users=friend)

        # End friendship :(
        elif action == 'remove':
            friendship = get_object_or_404(Friendship, main_user=current_user, friend_users=friend)
            friendship.delete()

        return JsonResponse({"result": True})