import urllib
import urllib2
import json
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.core.exceptions import ObjectDoesNotExist

from social_auth.models import UserSocialAuth
from profiles.models import FacebookProfile
from planning.models import Planning
from planning.tasks import find_where_to_go
from planning.forms import PlanningForm


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

    context = {
        'friends': friends,
        'form': form
    }
    return render(request, 'planning/friends_choose.html', context)


def friends_analize(request):
    if request.method == "POST":
        post_friends = request.POST.getlist('friends')
        friends = FacebookProfile.objects.filter(id__in=post_friends)
        context = {
            'friends': friends,
        }
        return render(request, 'planning/friends_analize.html', context)
    else:
        return HttpResponseForbidden()
