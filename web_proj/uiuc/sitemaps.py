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
from datetime import datetime
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from spacescout_web.spot import Spot


class SpotSitemap(Sitemap):
    changefreq = 'monthly'

    def __get(self, name, obj, *args, **kwargs):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return None
        if callable(attr):
            return attr(obj, *args, **kwargs)
        return attr

    def get_urls(self, page=1, site=None, protocol=None):
        # Determine protocol
        if self.protocol is not None:
            protocol = self.protocol
        if protocol is None:
            protocol = 'http'

        # Determine domain
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass
            if site is None:
                raise ImproperlyConfigured("To use sitemaps, either enable the sites framework or pass a Site/RequestSite object in your view.")
        domain = site.domain

        urls = []
        for item in self.paginator.page(page).object_list:
            loc = "%s://%s%s" % (protocol, domain, self.__get('location', item))
            priority = self.__get('priority', item)

            images = []
            for image in item.get('images', []):
                image_loc = "%s://%s%s" % (protocol, domain, self.__get('image_location', item, image))
                image_info = {
                    'image': image,
                    'location': image_loc,
                    'caption': self.__get('image_caption', item, image),
                    'title': self.__get('image_title', item, image),
                }
                images.append(image_info)

            url_info = {
                'item':       item,
                'location':   loc,
                'lastmod':    self.__get('lastmod', item),
                'changefreq': self.__get('changefreq', item),
                'priority':   str(priority is not None and priority or ''),
                'images':     images,
            }
            urls.append(url_info)
        return urls

    def items(self):
        return Spot.get_all()

    def lastmod(self, spot):
        return datetime.strptime(spot['server_last_modified'], '%Y-%m-%dT%H:%M:%S.%f')

    def location(self, spot):
        return reverse('share-url', kwargs={
            'spot_id': spot['id'],
            'spot_name': spot['name'],
        })

    def image_location(self, spot, image):
        return reverse('space-image-thumb', kwargs={
            'spot_id': spot['id'],
            'image_id': image['id'],
            'thumb_width': 300,
        })

    def image_caption(self, spot, image):
        return spot['name']

    def image_title(self, spot, image):
        return spot['name']
