from django.conf import settings
import re
from django.shortcuts import redirect, reverse


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, must-revalidate, no-store'
        response['Pragma'] = 'no-cache'
        response["Expires"] = "0"  # Proxies.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # page_nr = request.session.get('page_nr', 0)
        # assert hasattr(request, 'page_nr')
        #
        # if request.session['page_nr'] == 0:
        # return redirect(reverse('index'))
        path = request.path_info
        print(path)
