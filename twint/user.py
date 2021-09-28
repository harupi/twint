import datetime
import logging as logme


class user:
    type = "user"

    def __init__(self):
        pass


User_formats = {
    'join_date': '%Y-%m-%d',
    'join_time': '%H:%M:%S %Z'
}


# ur object must be a json from the endpoint https://api.twitter.com/graphql
def User(ur):
    logme.debug(__name__ + ':User')
    if 'data' not in ur and 'user' not in ur['data']:
        msg = 'malformed json! cannot be parsed to get user data'
        logme.fatal(msg)
        raise KeyError(msg)
    _usr = user()
    _usr.id = ur.get('data', {}).get('user', {}).get('rest_id')
    _usr.name = ur.get('data', {}).get('user', {}).get('legacy', {}).get('name')
    _usr.username = ur.get('data', {}).get('user', {}).get('legacy', {}).get('screen_name')
    _usr.bio = ur.get('data', {}).get('user', {}).get('legacy', {}).get('description')
    _usr.location = ur.get('data', {}).get('user', {}).get('legacy', {}).get('location')
    _usr.url = ur.get('data', {}).get('user', {}).get('legacy', {}).get('url')
    # parsing date to user-friendly format
    _dt = ur.get('data', {}).get('user', {}).get('legacy', {}).get('created_at')
    if _dt:
        _dt = datetime.datetime.strptime(_dt, '%a %b %d %H:%M:%S %z %Y')
        # date is of the format year,
    _usr.join_date = _dt.strftime(User_formats['join_date']) if _dt else ""
    _usr.join_time = _dt.strftime(User_formats['join_time']) if _dt else ""

    # :type `int`
    _tweets = ur.get('data', {}).get('user', {}).get('legacy', {}).get('statuses_count')
    _usr.tweets = int(_tweets) if _tweets else 0
    _following = ur.get('data', {}).get('user', {}).get('legacy', {}).get('friends_count')
    _usr.following = int(_following) if _following else 0
    _followers = ur.get('data', {}).get('user', {}).get('legacy', {}).get('followers_count')
    _usr.followers = int(_followers) if _followers else 0
    _likes = ur.get('data', {}).get('user', {}).get('legacy', {}).get('favourites_count')
    _usr.likes = int(_likes) if _likes else 0
    _media_count = ur.get('data', {}).get('user', {}).get('legacy', {}).get('media_count')
    _usr.media_count = int(_media_count) if _media_count else _media_count

    _usr.is_private = ur.get('data', {}).get('user', {}).get('legacy', {}).get('protected')
    _usr.is_verified = ur.get('data', {}).get('user', {}).get('legacy', {}).get('verified')
    _usr.avatar = ur.get('data', {}).get('user', {}).get('legacy', {}).get('profile_image_url_https')
    _usr.background_image = ur.get('data', {}).get('user', {}).get('legacy', {}).get('profile_banner_url')
    # TODO : future implementation
    # legacy_extended_profile is also available in some cases which can be used to get DOB of user
    return _usr
