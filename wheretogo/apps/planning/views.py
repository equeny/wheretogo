import urllib
import urllib2
import json
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from profiles.models import FacebookProfile


@login_required
def friends_choose(request):
    user = request.user
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
    context = {
        'friends': friends
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
