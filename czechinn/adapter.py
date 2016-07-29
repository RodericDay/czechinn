import requests

API_BASE = 'https://drchrono.com/api/'
AUTH_BASE = 'https://drchrono.com/o/authorize/'
CLIENT_ID = '2R23owlaoYG0YHz4pfr90s2DSXgHMnA8W2y277bg'
CLIENT_SECRET = 'iY4VctbA9xIjMsgoQXVO49KhZr9Vd5CHL4q7do5PneO2IoXPyQQZZAPdNHo3nfqf79N80xCp1iSCbHByAGap5FMNHo3fR9w5MGals75linTtJVPilV0zouTvDMvLrALC'
APP_URL = 'https://projects.roderic.ca'


def adapter(request, method, endpoint, extra=None):
    if extra and 'scheduled_time' in extra:
        extra['scheduled_time'] = extra['scheduled_time'].isoformat()

    access_token = request.user.profile.access_token
    headers = {'Authorization': "Bearer %s" % access_token}
    func = getattr(requests, method)
    response = func(API_BASE + endpoint, extra, headers=headers)
    response.raise_for_status()
    return response.json()
