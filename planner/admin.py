from django import forms
from django.contrib import admin
from django.forms import ModelChoiceField

from planner.models import Event, Participant, Map, EventMap, UserSocialAuthProxy
from social.apps.django_app.default.models import UserSocialAuth

from social.apps.django_app.default.admin import *

class EventAdmin(admin.ModelAdmin):
    pass


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.user.username


class PartForm(forms.ModelForm):
    player = MyModelChoiceField(queryset=UserSocialAuth.objects.all())
    class Meta:
        model = Participant


class ParticipantAdmin(admin.ModelAdmin):

    form = PartForm



class ProxyForm(forms.ModelForm):
    provider = forms.CharField(initial='steam')

    class Meta:
        model = UserSocialAuthProxy

    def clean(self):
        data = self.cleaned_data

        exists = UserSocialAuth.objects.filter(user=data['user'])
        if self.instance:
            exists = exists.exclude(pk=self.instance.pk)

        if exists:
            raise forms.ValidationError("Chosen user is already associated to some account")

        return data


class UserSocialAuthProxyAdmin(admin.ModelAdmin):

    form = ProxyForm

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Map)
admin.site.register(UserSocialAuthProxy, UserSocialAuthProxyAdmin)

try:
    admin.site.unregister(UserSocialAuth)
except:
    pass

try:
    admin.site.unregister(Nonce)
except:
    pass
