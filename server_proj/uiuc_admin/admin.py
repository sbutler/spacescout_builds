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

from django import forms
from django.conf import settings
from django.contrib import admin

from geoposition import Geoposition
from geoposition.forms import GeopositionField
from spotseeker_server.admin import SpotAdmin
from spotseeker_server.forms.spot import SpotForm as SSSpotForm, SpotExtendedInfoForm as SSSpotExtendedInfoForm
from spotseeker_server.models import SpotAvailableHours, SpotImage
import re

from .models import UIUCSpot, HostAuthRule

SpotForm = SSSpotForm.implementation()
SpotExtendedInfoForm = SSSpotExtendedInfoForm.implementation()

SPOT_BOOLEAN_FIELDS = (
    'has_whiteboards',
    'has_outlets',
    'has_printing',
    'has_scanner',
    'has_displays',
    'has_projector',
    'has_computers',
    'has_natural_light',
    'reservable',
    )

SPOT_INTEGER_FIELDS = (
    'num_computers',
    )

SPOT_STRING_FIELDS = (
    'campus',
    'uiuc_require_address',
    'uiuc_require_edutype',
    'food_allowed',
    'access_notes',
    'reservation_url',
    'reservation_notes',
    'location_description',
    )

UIUC_EDU_CHOICES = (
    ('', ''),
    ('person', 'Person'),
    ('phone', 'Phone'),
    ('staff', 'Staff'),
    ('student', 'Student'),
    ('allied', 'Allied'),
    ('extrahelp', 'Extra Help'),
    ('retired', 'Retired'),
    ('extramural', 'Extramural'),
    ('iei', 'IEI'),
    ('ews', 'EWS'),
    ('unihigh', 'University Highschool'),
    ('special', 'Special'),
    ('other', 'Other'),
    )

FOOD_ALLOWED = (
    ('', ''),
    ('none', 'No food allowed'),
    ('covered_drink', 'Covered drinks only'),
    ('any', 'All food allowed'),
    )

CAMPUSES = (
    ('uiuc', 'Urbana-Champaign'),
    ('uic', 'Chicago'),
    ('uis', 'Springfield'),
    )

class UIUCSpotAvailableHoursInline(admin.TabularInline):
    """ Inline hours form for the admin interface """
    model = SpotAvailableHours

class UIUCSpotImageInline(admin.StackedInline):
    """ Inline images form for the admin interface """
    model = SpotImage
    exclude = ('content_type', 'width', 'height', 'etag', 'upload_user', 'upload_application')
    extra = 1

class UIUCSpotForm(SpotForm):
    """
    Custom form that makes it easier to set the location for a
    spot and the extended info values that UIUC cares about.
    """
    coordinates = GeopositionField()
    has_whiteboards = forms.BooleanField(required=False)
    has_outlets = forms.BooleanField(required=False)
    has_printing = forms.BooleanField(required=False)
    has_scanner = forms.BooleanField(required=False)
    has_displays = forms.BooleanField(required=False)
    has_projector = forms.BooleanField(required=False)
    has_computers = forms.BooleanField(required=False)
    has_natural_light = forms.BooleanField(required=False)
    reservable = forms.BooleanField(required=False)
    num_computers = forms.IntegerField(required=False, label='Computer Count')
    uiuc_require_address = forms.CharField(required=False,
            label='Restrict by Address',
            help_text='Regular expression that matches the residential address of people allowed to use this space'
            )
    uiuc_require_edutype = forms.ChoiceField(required=False,
            choices=UIUC_EDU_CHOICES,
            label='Restrict by Type',
            help_text='Matches the uiucEduType field of people allowed to use this space'
            )
    access_notes = forms.CharField(required=False,
            help_text='Access notes to display on the space detailed view.'
            )
    reservation_url = forms.URLField(required=False,
            label='Reservation URL',
            help_text='URL that takes people to the reservation system.'
            )
    reservation_notes = forms.CharField(required=False,
            help_text='Reservation notes to display on the space detailed view.'
            )
    location_description = forms.CharField(required=False,
            help_text='Human readable location description.'
            )
    campus = forms.ChoiceField(required=True, choices=CAMPUSES)
    food_allowed = forms.ChoiceField(required=False, choices=FOOD_ALLOWED)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form fields with values from the spot and
        its extended information.
        """
        super(UIUCSpotForm, self).__init__(*args, **kwargs)

        self.fields['manager'].label = 'Manager Email'
        self.fields['manager'].help_text = 'Allows clients to report problems with the space.'
        self.fields['external_id'].label = 'External ID'

        spot = self.instance
        spot_ei = dict((ei.key, ei) for ei in spot.spotextendedinfo_set.all())

        # Make sure the map is centered properly, either with the
        # defaults or from the spot latitude/longitude
        if spot is None or spot.latitude is None or spot.longitude is None:
            if hasattr(settings, 'SS_DEFAULT_LOCATION'):
                defloc = settings.SS_LOCATIONS[settings.SS_DEFAULT_LOCATION]
                self.fields['coordinates'].initial = Geoposition(
                        defloc[ 'CENTER_LATITUDE' ],
                        defloc[ 'CENTER_LONGITUDE' ]
                        )
        else:
            self.fields['coordinates'].initial = Geoposition(
                    spot.latitude,
                    spot.longitude
                    )

        # Set all of the boolean extended info fields
        for field in SPOT_BOOLEAN_FIELDS:
            if field in spot_ei and spot_ei[field].value == 'true':
                self.fields[field].initial = True

        for field in SPOT_INTEGER_FIELDS:
            self.fields[field].widget.attrs['class'] = 'vIntegerField'
            if field in spot_ei:
                self.fields[field].initial = int(spot_ei[field].value)

        for field in SPOT_STRING_FIELDS:
            self.fields[field].widget.attrs['class'] = 'vTextField'
            if field in spot_ei:
                self.fields[field].initial = spot_ei[field].value

    def clean_uiuc_require_address(self):
        pattern = self.cleaned_data['uiuc_require_address']
        if pattern:
            try:
                re.compile(pattern)
            except:
                raise forms.ValidationError("Value must be a regular expression")
        return pattern

    class Meta:
        model = UIUCSpot
        exclude = ('latitude', 'longitude', 'etag',)

class UIUCSpotAdmin(SpotAdmin):
    """
    Admin model that uses the admin form and saves the extended information
    properly.
    """
    form = UIUCSpotForm
    fieldsets = (
            (None, {
                'fields': ('name', 'spottypes', 'organization', 'manager', 'external_id',)
                }
            ),
            ('Location', {
                'fields': ('campus', 'building_name', 'floor', 'room_number', 'coordinates',)
                }
            ),
            ('Features', {
                'fields': (
                    'capacity',
                    'num_computers',
                    'uiuc_require_address',
                    'uiuc_require_edutype',
                    'food_allowed',
                    ('has_whiteboards', 'has_outlets', 'has_printing'),
                    ('has_scanner', 'has_displays', 'has_projector'),
                    ('has_computers', 'has_natural_light', 'reservable'),
                    )
                }
            ),
            ('Notes', {
                'fields': ('access_notes', 'reservation_url', 'reservation_notes', 'location_description',)
                }
            ),
        )
    inlines = [UIUCSpotAvailableHoursInline, UIUCSpotImageInline]

    def save_model(self, request, spot, form, change):
        spot.latitude = form.cleaned_data['coordinates'][0]
        spot.longitude = form.cleaned_data['coordinates'][1]

        super(UIUCSpotAdmin, self).save_model(request, spot, form, change)

    def save_related(self, request, form, formsets, change):
        """ Pull out our custom fields and save them as extended info """
        super(UIUCSpotAdmin, self).save_related(request, form, formsets, change)

        spot = form.instance
        if not spot:
            return
        spot_ei = dict((ei.key, ei) for ei in spot.spotextendedinfo_set.all())

        # Update the boolean extended info fields
        for field in SPOT_BOOLEAN_FIELDS:
            if form.cleaned_data[field]:
                eiform = SpotExtendedInfoForm(
                    {'spot':spot.pk, 'key':field, 'value':'true'},
                    instance=spot_ei.get(field)
                )
                if eiform.is_valid():
                    eiform.save()
            else:
                if field in spot_ei:
                    spot_ei[field].delete()

        for field in SPOT_INTEGER_FIELDS:
            if form.cleaned_data[field] > 0:
                eiform = SpotExtendedInfoForm(
                    {'spot':spot.pk, 'key':field, 'value':form.cleaned_data[field]},
                    instance=spot_ei.get(field)
                )
                if eiform.is_valid():
                    eiform.save()
            else:
                if field in spot_ei:
                    spot_ei[field].delete()

        for field in SPOT_STRING_FIELDS:
            if form.cleaned_data[field]:
                eiform = SpotExtendedInfoForm(
                    {'spot':spot.pk, 'key':field, 'value':form.cleaned_data[field]},
                    instance=spot_ei.get(field)
                )
                if eiform.is_valid():
                    eiform.save()
            else:
                if field in spot_ei:
                    spot_ei[field].delete()

    def save_formset(self, request, form, formset, change):
        """ Add user and app info to SpotImages """
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, SpotImage):
                instance.upload_user = request.user.username
                instance.upload_application = 'UIUC Admin'
            instance.save()
        formset.save_m2m()

    class Media:
        css = {
            'all': ('uiuc_admin/uiuc_admin.css',)
            }

admin.site.register(UIUCSpot, UIUCSpotAdmin)

class HostAuthRuleAdmin(admin.ModelAdmin):
    readonly_fields = ('entry_type',)
    list_filter = (
            'kind',
            )
    list_display = (
            '__unicode__',
            'entry_type',
            )

admin.site.register(HostAuthRule, HostAuthRuleAdmin)
