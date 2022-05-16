from flask import Flask, render_template, json, request
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import os
import tweepy
import requests
import pandas as pd
from pprint import pprint


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')  # cosumer_key
API_KEY_SECRET = os.getenv('API_KEY_SECRET')  # consumer_secret
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
TWEEPY_CLIENT = None  # initialized to None

templates = os.path.abspath('templates')
app = Flask(__name__, template_folder=templates)
app.secret_key = BEARER_TOKEN

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


def set_tweepy_client(access_token):
    global TWEEPY_CLIENT
    TWEEPY_CLIENT = tweepy.Client(access_token,
                                  return_type=requests.Response,
                                  wait_on_rate_limit=True, )
    return TWEEPY_CLIENT


def get_tweepy_client() -> tweepy.Client:
    return globals()['TWEEPY_CLIENT']


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
    # following = client.get_users_followers(id=me['id']).json()['data']
    # pprint(me)
    # pprint(following)
    # endregion OAUTH 1.0a

    # region OAUTH 2.0
    consent = oauth2_user_handler.fetch_token(authorization_response=request.url)
    access_token = consent['access_token']
    refresh_token = consent['refresh_token']

    print('consent:')
    pprint(consent)

    client = set_tweepy_client(access_token=access_token)

    me = client.get_me(user_auth=False).json()['data']
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

    print('me:')
    pprint(me)
    # endregion OAUTH 2.0

    # region following
    following = []  # people I follow
    user_fields = ['created_at', 'description', 'id', 'location', 'name',
                   'pinned_tweet_id', 'profile_image_url', 'protected',
                   'url', 'username', 'verified', ]
    initial_request = client.get_users_following(id=my_id, max_results=1000, user_fields=user_fields).json()
    next_token = initial_request['meta']['next_token']

    while next_token is not None:
        following.extend(initial_request['data'])
        next_request = client.get_users_following(id=my_id,
                                                  max_results=1000,
                                                  user_fields=user_fields,
                                                  pagination_token=next_token).json()
        if 'meta' in next_request.keys():
            if 'next_token' in next_request['meta'].keys():
                next_token = next_request['meta']['next_token']
            else:
                next_token = None
                following.extend(next_request['data'])
                break
        initial_request = next_request
    # endregion following

    # region followers
    followers = []  # people following me
    user_fields = ['created_at', 'description', 'id', 'location', 'name',
                   'pinned_tweet_id', 'profile_image_url', 'protected',
                   'url', 'username', 'verified', ]
    initial_request = client.get_users_followers(id=my_id,  max_results=100, user_fields=user_fields).json()
    next_token = initial_request['meta']['next_token']

    while next_token is not None:
        followers.extend(initial_request['data'])
        next_request = client.get_users_followers(id=my_id,
                                                  max_results=100,
                                                  user_fields=user_fields,
                                                  pagination_token=next_token).json()
        if 'meta' in next_request.keys():
            if 'next_token' in next_request['meta'].keys():
                next_token = next_request['meta']['next_token']
            else:
                next_token = None
                followers.extend(next_request['data'])
                break
        initial_request = next_request
    # endregion

    # region save to disk
    today = datetime.strftime(datetime.today(), '%b-%d-%Y')
    df = pd.json_normalize(following)
    df.to_csv(f'static/following_{today}.csv')

    df = pd.json_normalize(followers)
    df.to_csv(f'static/followers_{today}.csv')
    # endregion

    return render_template('welcome.html', access_token=access_token)


@app.route('/unfollow')
def unfollow_view():
    return render_template('unfollow.html')


async def unfollow_non_followers(tweepy_client: tweepy.Client, non_followers_df: pd.DataFrame):
    print(f'[*] INITIATING MASS UNFOLLOW...')

    responses = []
    if tweepy_client is not None:
        for row in non_followers_df.itertuples(index=True, name='User'):
            res = tweepy_client.unfollow_user(target_user_id=int(row.user_id), user_auth=False)

            current_data = dict()
            current_data['user_id'] = row.user_id
            current_data['handle'] = row.username_x
            current_data['response'] = res.json()

            pprint(current_data)
            responses.append(current_data)

            # https://developer.twitter.com/en/docs/twitter-api/rate-limits
            await asyncio.sleep(20)  # time.sleep(18)
    return responses


@app.route('/execute-unfollow/', methods=['POST'])
async def execute_unfollow():
    # region non_followers pandas
    today = datetime.strftime(datetime.today(), '%b-%d-%Y')

    # Read dfs from disk:
    df_following = pd.read_csv(f'static/following_{today}.csv')
    df_followers = pd.read_csv(f'static/followers_{today}.csv')

    # Remove weird "Unnamed: 0" column
    if 'Unnamed: 0' in df_following.columns:
        df_following.drop(columns=['Unnamed: 0'], inplace=True)
    if 'Unnamed: 0' in df_followers.columns:
        df_followers.drop(columns=['Unnamed: 0'], inplace=True)

    # Renaming this column to distinguish it from index.
    renamed_columns = ({'id': 'user_id'})
    df_following.rename(columns=renamed_columns, inplace=True)
    df_followers.rename(columns=renamed_columns, inplace=True)

    # Cast user_id column type as `int64` type is not guaranteed. The column
    # datatype changes depending on if we read it from a file or not.
    df_following[['user_id']] = df_following[['user_id']].apply(pd.to_numeric, errors='coerce')
    df_followers[['user_id']] = df_followers[['user_id']].apply(pd.to_numeric, errors='coerce')

    non_followers = pd.merge(left=df_following, right=df_followers, how='left', on='user_id', indicator=True)
    non_followers = non_followers[non_followers['_merge'] == 'left_only']

    non_followers.to_csv(f'static/non_followers_{today}.csv')
    # endregion pandas

    # region execute unfollow
    non_followers = non_followers[['user_id', 'username_x']].reset_index(drop=True)
    data = await unfollow_non_followers(tweepy_client=get_tweepy_client(),
                                        non_followers_df=non_followers)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    # endregion
    return response


if __name__ == "__main__":
    app.run(debug=True)
