from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import HttpRequest
from dotenv import load_dotenv
from pprint import pprint
import os
import tweepy
import requests
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import TwitterUser


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')  # cosumer_key
API_KEY_SECRET = os.getenv('API_KEY_SECRET')  # consumer_secret
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')



#### OAUTH 1.0a ####
# oauth1_user_handler = tweepy.OAuth1UserHandler(
#     consumer_key=API_KEY,
#     consumer_secret=API_KEY_SECRET,
#     # access_token=ACCESS_TOKEN,
#     # access_token_secret=ACCESS_TOKEN_SECRET,
#     callback='http://127.0.0.1:5000/welcome',
#     )
#
# auth_url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

#### OAUTH 2.0 ####
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="http://127.0.0.1:5000/welcome",
    scope=[
           # "block.read",
           # "block.write",
           "follows.read",
           "follows.write",
           # "like.read",
           # "like.write",
           # "list.read",
           # "list.write",
           # "mute.read",
           # "mute.write"
           "offline.access",
           # "space.read",
           # "space.write",
           "tweet.read",
           "tweet.write",
           # "tweet.moderate.write"
           "users.read",
           ],
    client_secret=CLIENT_SECRET,
)
auth_url = oauth2_user_handler.get_authorization_url()


def home(request):
    context = {
        'auth_url': auth_url
    }
    return render(request, template_name='dashboard/home.html', context=context)


def welcome(request):
    #### OAUTH 1.0a ####
    # query_str_args = request.args.to_dict()
    # oauth_token = query_str_args['oauth_token']
    # oauth_verifier = query_str_args['oauth_verifier']
    #
    # access_token, access_token_secret = oauth1_user_handler.\
    #     get_access_token(oauth_verifier)
    #
    # print(f'access_token: {access_token}')
    # print(f'access_token_secret: {access_token_secret}')
    #
    # client = tweepy.Client(
    #     bearer_token=BEARER_TOKEN,
    #     consumer_key=API_KEY,
    #     consumer_secret=API_KEY_SECRET,
    #     access_token=access_token,
    #     access_token_secret=access_token_secret,
    #     return_type=requests.Response,
    #     wait_on_rate_limit=True
    # )
    #
    # me = client.get_me().json()['data']
    # people_i_follow = client.get_users_followers(id=me['id']).json()['data']
    # pprint(me)
    # pprint(people_i_follow)

    #### OAUTH 2.0 ####
    consent = oauth2_user_handler.fetch_token(authorization_response=request.url)
    access_token = consent['access_token']
    refresh_token = consent['refresh_token']

    print('consent:')
    pprint(consent)

    client = tweepy.Client(access_token,
                           return_type=requests.Response,
                           wait_on_rate_limit=True,)

    # client = tweepy.Client(
    #     bearer_token=f'Bearer {access_token}',
    #     consumer_key=API_KEY,
    #     consumer_secret=API_KEY_SECRET,
    #     access_token=access_token,
    #     # access_token_secret=access_token_secret,
    #     return_type=requests.Response,
    #     wait_on_rate_limit=True
    # )

    me = client.get_me(user_auth=False).json()['data']
    people_i_follow = client.get_users_followers(id=me['id']).json()['data']
    pprint(me)
    pprint(people_i_follow)

    context = {
        'access_token': access_token,
    }

    return render(request=HttpRequest(), template_name='dashboard/home.html', context=context)

# class TwitterUserListView(ListView):
#     model = TwitterUser
#     template_name = 'dashboard/home.html'  # <app> /<model>_<viewtype>.html
#     context_object_name = 'twitter_users'

