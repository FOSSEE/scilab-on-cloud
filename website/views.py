from django.shortcuts import render 
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
	print('hi')
	context = {}
	return render(request, 'website/templates/login.html', context)

