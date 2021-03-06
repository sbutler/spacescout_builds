""" Copyright 2015 University of Illinois Board of Trustees

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic.base import RedirectView
from django.utils.http import urlquote

from shibboleth.app_settings import LOGOUT_REDIRECT_URL, LOGOUT_SESSION_KEY

class LoginView(RedirectView):
    """
    Redirect the user to the Shibboleth login URL.
    """
    def get(self, request, *args, **kwargs):
        # Remove session value that is forcing Shibboleth reauthentication.
        request.session.pop(LOGOUT_SESSION_KEY, None)
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        target = self.request.GET.get(REDIRECT_FIELD_NAME, '/')

        return settings.SHIBBOLETH_LOGIN_URL % urlquote(target)


class LogoutView(RedirectView):
    """
    Redirect the user to the Shibboleth logout URL.
    """
    def get(self, request, *args, **kwargs):
        #Log the user out.
        auth.logout(self.request)

        #Set session key that middleware will use to force 
        #Shibboleth reauthentication.
        self.request.session[LOGOUT_SESSION_KEY] = True

        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        target = LOGOUT_REDIRECT_URL
        if not target:
            target = self.request.GET.get(REDIRECT_FIELD_NAME, '/')

        return settings.SHIBBOLETH_LOGOUT_URL % urlquote(target)
