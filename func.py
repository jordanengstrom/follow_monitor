import pandas as pd
import os
from datetime import datetime, timedelta
from twarc.client2 import Twarc2
from dotenv import load_dotenv


# Setup environment
load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')  # cosumer_key
API_KEY_SECRET = os.getenv('API_KEY_SECRET')  # consumer_secret
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
MY_ID = int(os.getenv('MY_ID'))

# Setup client
t = Twarc2(consumer_key=API_KEY, consumer_secret=API_KEY_SECRET,
           access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET,
           bearer_token=BEARER_TOKEN, )


def fetch_twitter_data() -> list:
    """
    Uses the twarc library to obtain data of the people I follow.
    """
    users_i_follow = []
    data_generator = t.following(user=MY_ID)

    # Use generator to repeatedly get the next list of users:
    for obj in data_generator:
        users_i_follow.extend(obj['data']) if 'data' in obj.keys() \
            else users_i_follow.extend(obj['errors'])

    return users_i_follow


def get_dataframes() -> tuple:
    """
    This function obtains the data of interest, puts it into
    two pd.DataFrames, and returns a tuple like so:
    (today: pd.DataFrame, yesterday: pd.DataFrame)
    """

    # Initialize dates we will use:
    today = datetime.strftime(datetime.today(), '%b-%-d-%Y')
    yesterday = datetime.strftime((datetime.today() + timedelta(days=-1)), '%b-%-d-%Y')
    two_days_ago = datetime.strftime((datetime.today() + timedelta(days=-2)), '%b-%-d-%Y')

    # Get twitter data and save to csv, this is today's df
    # following_today = fetch_twitter_data()
    # todays_data = pd.json_normalize(following_today)
    # todays_data.to_csv(f'static/{today}.csv')

    # From disk:
    todays_data = pd.read_csv(f'static/{today}.csv')

    # Read yesterday's df from file:
    yesterdays_data = pd.read_csv(f'static/{yesterday}.csv')

    # Remove file from two days ago if it exists:
    # FIXME: Ok to uncomment when ready to launch:
    # try:
    #     os.remove(f'static/{two_days_ago}.csv')
    # except FileNotFoundError:
    #     pass

    return todays_data, yesterdays_data


def plant_bad_seed(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function was created as a sanity check. I wanted to
    write a function to plant a difference and see what
    happens to the behavior of the `is_following_list_identical()` function.
    """
    bad_seed = {
        'description': ['some test person'],
        'name': ['john doe'],
        'location': ['somewhere idk'],
        'profile_image_url': ['https://picsum.photos/id/237/200/300'],
        'url': [''],
        'verified': [False],
        'protected': [False],
        'id': ['666'],
        'username': ['jd'],
        'created_at': [datetime.now()],
    }
    bad_df = pd.DataFrame(bad_seed)
    return pd.concat([df, bad_df], ignore_index=True, axis=0)


def is_following_list_identical(todays_df: pd.DataFrame, yesterdays_df: pd.DataFrame) -> tuple:
    # Default data contains a lot of extra columns, so they are dropped:
    extra_columns = ['entities.url.urls', 'entities.description.urls',
                     'public_metrics.followers_count', 'public_metrics.following_count',
                     'public_metrics.tweet_count', 'public_metrics.listed_count',
                     'entities.description.hashtags', 'entities.description.mentions',
                     'pinned_tweet_id', 'entities.description.cashtags',
                     ]
    todays_df.drop(columns=extra_columns, inplace=True)
    yesterdays_df.drop(columns=extra_columns, inplace=True)

    if 'Unnamed: 0' in todays_df.columns:
        todays_df.drop(columns=['Unnamed: 0'], inplace=True)
    if 'Unnamed: 0' in yesterdays_df.columns:
        yesterdays_df.drop(columns=['Unnamed: 0'], inplace=True)

    print('todays_df.columns:')
    print(todays_df.columns)

    # Renaming this column to distinguish it from index.
    renamed_columns = ({'id': 'user_id'})
    todays_df.rename(columns=renamed_columns, inplace=True)
    yesterdays_df.rename(columns=renamed_columns, inplace=True)

    # Cast user_id column type as `int64` type is not guaranteed. The column
    # datatype changes depending on if we read it from a file or not.
    todays_df[['user_id']] = todays_df[['user_id']].apply(pd.to_numeric, errors='coerce')
    yesterdays_df[['user_id']] = yesterdays_df[['user_id']].apply(pd.to_numeric, errors='coerce')

    # To find differences that exist in either dataframe, we use
    # something called a "symmetric difference" between two sets.
    # We can assume each user_id is unique, so that's what we use for comparison.
    # https://www.adamsmith.haus/python/answers/how-to-get-the-symmetric-difference-of-pandas-dataframes-in-python
    union = pd.concat([todays_df, yesterdays_df], axis=0)
    sym_diff = union.drop_duplicates(subset='user_id', keep=False, inplace=False)

    yesterday_only = pd.merge(left=yesterdays_df, right=todays_df, how='left', on='user_id', indicator=True)
    yesterday_only = yesterday_only[yesterday_only['_merge'] == 'left_only']

    today_only = pd.merge(left=todays_df, right=yesterdays_df, how='left', on='user_id', indicator=True)
    today_only = today_only[today_only['_merge'] == 'left_only']

    no_diff = len(sym_diff) == 0  # if empty, there are no differences
    if no_diff:
        return False, yesterday_only, today_only, sym_diff
    else:
        return True, yesterday_only, today_only, sym_diff


td_df, yd_df = get_dataframes()
# td_df = plant_bad_seed(td_df)  # use to test
# yd_df = plant_bad_seed(yd_df)  # use to test
results = is_following_list_identical(todays_df=td_df, yesterdays_df=yd_df)
