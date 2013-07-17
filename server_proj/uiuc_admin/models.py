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

