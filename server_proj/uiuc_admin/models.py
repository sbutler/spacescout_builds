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
"""

from django.db import models
import ipaddress

from spotseeker_server.models import Spot

class UIUCSpot(Spot):
    """
    Proxy model for a Spot so that we can register
    with the admin inferface twice.
    """
    class Meta:
        proxy = True
        verbose_name = 'UIUC Spot'
        verbose_name_plural = 'UIUC Spots'
        app_label = 'spotseeker_server'

class HostAuthRule(models.Model):
    """
    Host record (and its permissions) for authenticating the REST API.
    """

    ENTRY_TYPE_CHOICES = (
            ('ip_address', 'IP Address'),
            ('ip_network', 'IP Network'),
            ('host_suffix', 'Host Suffix'),
            ('host_exact', 'Host Exact'),
            )
    ACCESS_CHOICES = (
            ('allow', 'Allow'),
            ('deny', 'Deny'),
            )
    KIND_CHOICES = (
            ('application', 'Application'),
            ('user', 'User'),
            )

    entry = models.CharField(max_length=100, blank=False)
    entry_type = models.CharField(max_length=100, choices=ENTRY_TYPE_CHOICES, blank=True)
    access = models.CharField(max_length=100, choices=ACCESS_CHOICES, blank=False)
    kind = models.CharField(max_length=100, choices=KIND_CHOICES, blank=False, db_index=True)

    def __unicode__(self):
        return "{0} as {1} from {2}".format(self.access, self.kind, self.entry)

    def matches(self, remote_address, remote_host):
        if remote_address is None:
            return False

        if self.entry_type == 'host_suffix':
            if not remote_host:
                return False
            else:
                return remote_host.endswith(self.entry)

        elif self.entry_type == 'host_exact':
            if not remote_host:
                return False
            else:
                return remote_host == self.entry

        elif self.entry_type == 'ip_address':
            return remote_address == ipaddress.ip_address(self.entry)

        elif self.entry_type == 'ip_network':
            return remote_address in ipaddress.ip_network(self.entry)

        return False

    def save(self, *args, **kwargs):
        entry_type = None
        if entry_type is None:
            try:
                if ipaddress.ip_address(self.entry):
                    entry_type = 'ip_address'
            except ValueError:
                pass

        if entry_type is None:
            try:
                if ipaddress.ip_network(self.entry):
                    entry_type = 'ip_network'
            except ValueError:
                pass

        if entry_type is None:
            if self.entry.startswith('.'):
                entry_type = 'host_suffix'
            else:
                entry_type = 'host_exact'

        self.entry_type = entry_type

        super(HostAuthRule, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Host Authentication Rule"
        verbose_name_plural = "Host Authentication Rules"

