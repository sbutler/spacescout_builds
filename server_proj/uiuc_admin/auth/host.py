""" Copyright 2013 University of Illinois Board of Trustees

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Authenticate access based on the remote host/address.
"""

from django.http import HttpResponse
import ipaddress
import socket

from ..models import HostAuthRule

def _allow_deny(rules, remote_address, remote_host):
    """
    Checks the rules using the following process:
        1. Match allow rules until one is found. If none match then return False
        2. Match all deny rules. If any match then False is returned
        3. Return True
    """

    matches = False
    for rule in rules.filter(access='allow'):
        if rule.matches(remote_address, remote_host):
            matches = True
            break

    if not matches:
        return False

    for rule in rules.filter(access='deny'):
        if rule.matches(remote_address, remote_host):
            return False

    return True

def _deny_allow(rules, remote_address, remote_host):
    """
    Checks the rules using the following process:
        1. Match deny rules until one is found. If none matches then return True
        2. Match all allow rules. If any match then True is returned
        3. Return False
    """

    matches = False
    for rule in rules.filter(access='deny'):
        if rule.matches(remote_address, remote_host):
            matches = True
            break

    if not matches:
        return True

    for rule in rules.filter(access='allow'):
        if rule.matches(remote_address, remote_host):
            return True

    return False

def _get_remote_host(request):
    """
    Try to get the remote host from the request, resolving
    if we need to.
    """
    result = request.META.get('REMOTE_HOST', None)
    if not result:
        try:
            hostinfo = socket.gethostbyaddr(request.META['REMOTE_ADDR'])
            result = hostinfo[0]
        except socket.error as err:
            if err[0] != 1:
                raise

    return result


def authenticate_application(view, request, *args, **kwargs):
    """ Allows all hosts, unless one is specifically denied. """
    rules = HostAuthRule.objects.filter(kind='application')

    remote_address = ipaddress.ip_address(request.META['REMOTE_ADDR'].decode('ascii'))
    remote_host = _get_remote_host(request)

    if not _deny_allow(rules, remote_address, remote_host):
        return HttpResponse("Error authenticating application", status=401)

    return


def authenticate_user(view, request, *args, **kwargs):
    """ Denies all hosts, unless one is specifically allowed. """
    rules = HostAuthRule.objects.filter(kind='user')

    remote_address = ipaddress.ip_address(request.META['REMOTE_ADDR'].decode('ascii'))
    remote_host = _get_remote_host(request)

    if not _allow_deny(rules, remote_address, remote_host):
        return HttpResponse("Error authenticating user", status=401)

    return
