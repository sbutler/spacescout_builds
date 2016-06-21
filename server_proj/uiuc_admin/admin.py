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
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from geoposition import Geoposition
from geoposition.forms import GeopositionField
import logging
from spotseeker_server.admin import SpotAdmin
from spotseeker_server.forms.spot import SpotForm as SSSpotForm, SpotExtendedInfoForm as SSSpotExtendedInfoForm
from spotseeker_server.models import SpotAvailableHours, SpotImage, SpaceReview
import re

from .models import UIUCSpot, UIUCSpaceReview, HostAuthRule

logger = logging.getLogger(__name__)

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
    'noise_level',
    'access_notes',
    'reservation_url',
    'reservation_notes',
    'location_description',
    'mail_address',
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

NOISE_LEVEL = (
    ('', ''),
    ('silent', 'Silent'),
    ('quiet', 'Quiet (Low hum)'),
    ('moderate', 'Moderate (Chatter)'),
    ('loud', 'Loud'),
    ('variable', 'Variable'),
    )

CAMPUSES = (
    ('uiuc', 'Urbana-Champaign'),
    ('uic', 'Chicago'),
    ('uis', 'Springfield'),
    )


@receiver(pre_save, sender=SpaceReview)
def pre_save_space_review(sender, instance, raw, **kwargs):
    """ Copy the original review to the review field if new. """
    if raw or instance.pk:
        return

    if not instance.review:
        instance.review = instance.original_review

@receiver(post_save, sender=SpaceReview)
def post_save_space_review(sender, instance, created, raw, **kwargs):
    """
    Send an email when a new review has been saved to the
    space admins.
    """
    if raw or not created:
        return

    try:
        to_addr = instance.space.manager
        if not to_addr:
            to_addr = getattr(settings, 'SPACESCOUT_REVIEW_MANAGERS', None)

        # Split the addresses apart if we have multiple
        recipient_list = []
        if to_addr:
            for addr in re.split(r'\s*,\s*', to_addr):
                if addr:
                    recipient_list.append(addr)

        if len(recipient_list):
            send_mail(
                subject='New Space Review: {0}'.format(instance.space),
                message='A new space review has been submitted.\n\nSpace: {0}\nReviewer: {1}\nRating: {2}\n\nVisit https://{3}{4} to moderate the review.'.format(
                    instance.space,
                    instance.reviewer,
                    instance.rating,
                    Site.objects.get(pk=settings.SITE_ID).domain,
                    reverse('admin:spotseeker_server_uiucspacereview_change', args=(instance.pk,)),
                ),
                recipient_list=recipient_list,
                from_email=getattr(settings, 'SPACESCOUT_REVIEW_MANAGERS', None),
            )
    except:
        logger.exception("Unable to notify managers of new space review {0}".format(instance.pk))


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
    access_notes = forms.CharField(widget=forms.Textarea, required=False,
            help_text='Access notes to display on the space detailed view. Limited HTML is allowed.'
            )
    reservation_url = forms.URLField(required=False,
            label='Reservation URL',
            help_text='URL that takes people to the reservation system.'
            )
    reservation_notes = forms.CharField(widget=forms.Textarea, required=False,
            help_text='Reservation notes to display on the space detailed view. Limited HTML is allowed.'
            )
    location_description = forms.CharField(required=False,
            help_text='Human readable location description that will be displayed on the results list.'
            )
    mail_address = forms.CharField(required=False,
            help_text='Mail address that will be displayed on the details page.'
            )
    campus = forms.ChoiceField(required=True, choices=CAMPUSES)
    food_allowed = forms.ChoiceField(required=False, choices=FOOD_ALLOWED)
    noise_level = forms.ChoiceField(required=False, choices=NOISE_LEVEL)

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

class UIUCSpaceReviewForm(forms.ModelForm):
    """
    Override some form fields from the default admin form.
    """
    class Meta:
        model = UIUCSpaceReview
        widgets = {
            'review': forms.Textarea(),
            'original_review': forms.Textarea(),
        }



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
                'fields': ('campus', 'building_name', 'floor', 'room_number', 'mail_address', 'coordinates',)
                }
            ),
            ('Features', {
                'fields': (
                    'capacity',
                    'num_computers',
                    'uiuc_require_address',
                    'uiuc_require_edutype',
                    'food_allowed',
                    'noise_level',
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
    ordering = ('name',)

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

class UIUCSpaceReviewAdmin(admin.ModelAdmin):
    """
    Admin model that uses the admin form and saves the space reviews
    properly.
    """
    form = UIUCSpaceReviewForm
    readonly_fields = (
        'space',
        'reviewer',
        'published_by',
        'original_review',
        'rating',
        'date_published',
    )
    list_display = (
        'space',
        'reviewer',
        'rating',
        'is_published',
        'date_published',
    )
    ordering = ('-date_published',)
    fieldsets = (
        ('General', {
            'fields': (('space', 'reviewer'), ('published_by', 'date_published')),
        }),
        ('Information', {
            'fields': ('rating', 'original_review', 'review', ('is_published', 'is_deleted')),
        }),
    )

    def save_model(self, request, obj, form, change):
        """ Do some custom actions around saving. """
        from spotseeker_server.views.reviews import update_review

        update_review(obj, request.user, data={
            'review': form.cleaned_data['review'],
            'publish': form.cleaned_data['is_published'],
            'delete': form.cleaned_data['is_deleted'],
        })

admin.site.register(UIUCSpaceReview, UIUCSpaceReviewAdmin)

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
