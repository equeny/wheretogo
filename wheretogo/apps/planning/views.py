import urllib
import urllib2
import json
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

from profiles.models import FacebookProfile
from planning.models import Planning, PlanningResultPlace, UserRating, Place
from planning.tasks import find_where_to_go
from planning.forms import PlanningForm

PLACE_MARKS = {
    'first_mark_code': 1,
    'second_mark_code': 2,
    'third_mark_code': 3
}


@login_required
def friends_choose(request):
    user = request.user
    # try:
    #     fb_user = FacebookProfile.objects.get(user=user)
    # except ObjectDoesNotExist:
    #     try:
    #         social_user = UserSocialAuth.objects.get(user=user)
    #         fb_user = FacebookProfile.objects.get_create(
    #             user=user,
    #             oauth_token=social_user.tokens['access_token'],
    #         )
    #     except UserSocialAuth.DoesNotExist:
    #         raise Http404

    oauth_token = user.fb_user.oauth_token
    friends = user.friends.all()
    week_ago = date.today() - timedelta(7)
    if not friends or user.fb_user.last_friends_update < week_ago:
        path = 'https://graph.facebook.com/me/friends?%s' % urllib.urlencode({
            'access_token': oauth_token,
            'fields': 'name,id,picture',
            'limit': 1000,
        })
        response = urllib2.urlopen(path)
        friends = json.loads(response.read())['data']
        for friend in friends:
            fr, created = FacebookProfile.objects.get_or_create(
                fid=friend['id'],
                name=friend['name'],
                picture=friend['picture'],
            )
            user.friends.add(fr)

    form = PlanningForm(
        request.POST or None, instance=Planning(organizer=user.fb_user)
    )
    if request.method == 'POST':
        if form.is_valid():
            planning = form.save()
            find_where_to_go.delay(planning)
            return redirect('planning_status', planning.id)

    context = {
        'friends': friends,
        'form': form
    }
    return render(request, 'planning/friends_choose.html', context)


@login_required
def friends_analize(request):
    if request.method == "POST":
        friends = FacebookProfile.objects.filter(id__in=request.POST.getlist('friends'))
        planning, created = Planning.objects.get_or_create(
            organizer=request.user.fb_user,
        )
        results = PlanningResultPlace.objects.filter(planning=planning)
        context = {
            'friends': friends,
            'results': results
        }
        return render(request, 'planning/friends_analize.html', context)
    else:
        return HttpResponseForbidden()


@login_required
def planning_list(request):
    results = Planning.objects.filter(
        Q(organizer=request.user.fb_user) | Q(profiles=request.user.fb_user)
    ).distinct()
    context = {
        'results': results,
    }
    return render(request, 'planning/planning_list.html', context)


@login_required
def planning_status(request, id):
    planning = get_object_or_404(Planning, id=id)
    # TODO: add permissions check

    if planning.status == Planning.STATUS_DONE:
        pass
        # redirect to results
    return render(request, 'planning/planning_status.html', {'planning': planning})


@login_required
def planning_results(request, id):
    planning = get_object_or_404(Planning, id=id)
    return render(request, 'planning/planning_results.html', {'planning': planning})


@login_required
def place_rate(request, plan_id, place_id):
    planning = Planning.objects.get(id=plan_id)
    value = request.GET['code']
    if value in PLACE_MARKS:
        UserRating.objects.filter(
            user=request.user,
            plan__id=planning.id,
            number=PLACE_MARKS[value]
        ).delete()
        try:
            rate = UserRating.objects.get(user=request.user, place__id=place_id, plan__id=plan_id)
            rate.number = PLACE_MARKS[value]
            rate.save()
        except UserRating.DoesNotExist:
            rate = UserRating.objects.create(
                user=request.user,
                place=Place.objects.get(id=place_id),
                plan=planning,
                number=PLACE_MARKS[value]
            )
        return redirect('planning_results', planning.id)
