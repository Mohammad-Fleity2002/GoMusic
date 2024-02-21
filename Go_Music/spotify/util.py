from datetime import timedelta
from django.utils import timezone
from requests import post, put, get, exceptions
from .credientials import CLIENT_ID, CLIENT_SECRET
from .models import SpotifyToken


BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

# store user info and update them


# def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
#     tokens = get_user_tokens(session_id)
#     expires_in = timezone.now() + timedelta(seconds=3600)
#     # storing the date when the session expire
#     if tokens:
#         tokens.access_token = access_token
#         tokens.refresh_token = refresh_token
#         tokens.expires_in = expires_in
#         tokens.token_type = token_type
#         tokens.save(update_fields=['access_token',
#                                    'refresh_token', 'expires_in', 'token_type'])
#         # updating
#     else:
#         # creating
#         tokens = SpotifyToken(user=session_id, access_token=access_token,
#                               refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
#         tokens.save()


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token, error):
    tokens = get_user_tokens(session_id)
    if error:
        print(error)
    else:
        expires_at = timezone.now() + timedelta(seconds=(3600*24))
        # print(expires_at)
        if tokens:
            tokens.access_token = access_token
            tokens.refresh_token = refresh_token
            tokens.expires_in = expires_at  # Update with calculated expiry time
            tokens.token_type = token_type
            tokens.save(update_fields=['access_token',
                        'refresh_token', 'expires_in', 'token_type'])
        else:
            tokens = SpotifyToken(user=session_id, access_token=access_token,
                                  refresh_token=refresh_token, token_type=token_type, expires_in=expires_at)
            tokens.save()
        # print(tokens)


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
            # update_or_create_user_tokens(
            #     session_id, tokens.access_token, tokens.token_type, tokens.expires_in, tokens.refresh_token, None)

        return True

    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    error = response.get('error')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token, error)


# def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False, data=None):
#     tokens = get_user_tokens(session_id)
#     headers = {'Content-Type': 'application/json',
#                'Authorization': "Bearer " + tokens.access_token}

#     if post_:
#         post(BASE_URL + endpoint, headers=headers, json=data)
#     if put_:
#         put(BASE_URL + endpoint, headers=headers, json=data)
#         print(headers)

#     response = get(BASE_URL + endpoint, headers=headers)
#     try:
#         return response.json()
#     except Exception as e:
#         return {f'Error': 'Issue with request: {str(e)}'}


def play_song(session_id):
    return execute_spotify_api_request(session_id, "player/play", put_=True)


def pause_song(session_id):
    return execute_spotify_api_request(session_id, "player/pause", put_=True)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False, data=None):
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + tokens.access_token
    }

    try:
        if post_:
            response = post(BASE_URL + endpoint, headers=headers, json=data)
        elif put_:
            response = put(BASE_URL + endpoint, headers=headers, json=data)
        else:
            response = get(BASE_URL + endpoint, headers=headers)
        print(response)
        # if response.status_code == 403:
        #     print(response.error.message)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except exceptions.RequestException as e:
        return {'Error': f'Request error: {str(e)}'}
    except Exception as ex:
        return {'Error': f'Unknown error: {str(ex)}'}
