from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from pprint import pprint
import itertools
import os
import tweepy
import requests
import pandas as pd

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')  # cosumer_key
API_KEY_SECRET = os.getenv('API_KEY_SECRET')  # consumer_secret
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

templates = os.path.abspath('templates')
app = Flask(__name__, template_folder=templates)

# region OAUTH 1.0a
# oauth1_user_handler = tweepy.OAuth1UserHandler(
#     consumer_key=API_KEY,
#     consumer_secret=API_KEY_SECRET,
#     # access_token=ACCESS_TOKEN,
#     # access_token_secret=ACCESS_TOKEN_SECRET,
#     callback='http://127.0.0.1:5000/welcome',
#     )
#
# auth_url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
# endregion OAUTH 1.0a


# region OAUTH 2.0
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


# endregion OAUTH 2.0


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', value=auth_url)


@app.route('/welcome', methods=['GET'])
def welcome():
    # region OAUTH 1.0a
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
    # endregion OAUTH 1.0a

    # region OAUTH 2.0
    consent = oauth2_user_handler.fetch_token(authorization_response=request.url)
    access_token = consent['access_token']
    refresh_token = consent['refresh_token']

    print('consent:')
    pprint(consent)

    client = tweepy.Client(access_token,
                           return_type=requests.Response,
                           wait_on_rate_limit=True, )

    me = client.get_me(user_auth=False).json()['data']
    print('me:')
    pprint(me)
    my_id = int(me['id'])

    people_i_follow = []
    user_fields = ['created_at', 'description', 'id', 'location', 'name',
                   'pinned_tweet_id', 'profile_image_url', 'protected',
                   'url', 'username', 'verified', ]
    initial_request = client.get_users_following(id=my_id, max_results=1000, user_fields=user_fields).json()
    next_token = initial_request['meta']['next_token']

    while next_token is not None:
        people_i_follow.extend(initial_request['data'])
        next_request = client.get_users_following(id=my_id,
                                                  max_results=1000,
                                                  user_fields=user_fields,
                                                  pagination_token=next_token).json()
        if 'meta' in next_request.keys():
            if 'next_token' in next_request['meta'].keys():
                next_token = next_request['meta']['next_token']
            else:
                next_token = None
                people_i_follow.extend(next_request['data'])
                break
        initial_request = next_request

    # pprint(people_i_follow)
    # endregion OAUTH 2.0

    # region pandas
    # df = pd.json_normalize(people_i_follow)
    # df.to_csv('people_i_follow.csv')
    #
    # print(f'LEN: {len(people_i_follow)}')
    # print(df.head())
    # endregion pandas

    return render_template('welcome.html', access_token=access_token)


@app.route('/following')
def following():
    pass


if __name__ == "__main__":
    app.run(debug=True)
