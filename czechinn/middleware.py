from django.conf import settings
from django.http import HttpResponseRedirect


class LoginRequiredEverywhereMiddleware:

    def process_request(self, request):
        if 'czechinn' in request.path and not request.user.is_authenticated():
            if request.path_info != settings.LOGIN_URL:
                return HttpResponseRedirect(settings.LOGIN_URL)
