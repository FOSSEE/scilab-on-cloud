from django.shortcuts import render 
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from website.models import TextbookCompanionPreference, \
    TextbookCompanionProposal, TextbookCompanionChapter, TextbookCompanionRevision

import requests

def index(request):
    context = {}
    user = request.user

    if not user.is_anonymous():
        social = user.social_auth.get(provider='google-oauth2')
        url = 'https://www.googleapis.com/plus/v1/people/me'
        params = {'access_token' : social.extra_data['access_token']}
        # r = requests.get(url, params=params)
        # print(r.content)

        context = {
        	'user' : user
        }

    return render(request, 'website/templates/index.html', context)

def login(request):
	context = {}
	return render(request, 'website/templates/login.html', context)

@user_passes_test(lambda u: u.is_staff)
def review(request):
    revisions = TextbookCompanionRevision.objects \
        .filter(push_status=0)\
        .order_by('timestamp')
    context = {
        'user': request.user,
        'revisions': revisions,
    }
    return render(request, 'website/templates/review-interface.html', context)