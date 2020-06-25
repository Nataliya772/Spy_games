from urllib.parse import urlencode

def get_token():
    id = int(input('Укажите id: '))
    OAUTH_URL = 'https://oauth.vk.com/authorize'
    OAUTH_PARAMS = {
        'client_id': id,
        'display': 'page',
        'scope': 'friends, groups',
        'response_type': 'token',
        'v': 5.89
    }

    print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))

get_token()