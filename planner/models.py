from django.core.cache import cache
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from social.apps.django_app.default.models import UserSocialAuth


STATUS_CHOICES = (
    ('com', _("Commander")),
    ('yes', _("Player")),
    ('may', _("?")),
    ('no', _("No")),
)

STATUS_STORY = (
    ('com', _("Yes, as a commander")),
    ('yes', _("Yes, as a player")),
    ('may',  _("I'm not sure")),
    ('no', _("No")),
)

class EventMap(models.Model):
    participant = models.ForeignKey('planner.Participant')
    map = models.ForeignKey('planner.Map')
    event = models.ForeignKey('planner.Event')

    class Meta:
        unique_together = ('participant', 'map', 'event')

    def __unicode__(self):
        return u"%s voted for %s" % (self.participant, self.map.name)


class Participant(models.Model):
    player = models.ForeignKey(UserSocialAuth)
    event = models.ForeignKey('planner.Event')
    status = models.CharField(_("Status"), max_length=3, choices=STATUS_CHOICES)
    maps = models.ManyToManyField('planner.Map', through=EventMap)

    class Meta:
        unique_together = (
            ('player', 'event'),
        )

    def save(self, *args, **kwargs):
        super(Participant, self).save(*args, **kwargs)

        cache.set('attend-%s-%s' % (self.event.pk, self.player.pk), self.status)
        cache.set('attend-count-%s' % self.player.pk, None)

    def __unicode__(self):
        return u"%s - %s (%s)" % (
        self.event.when.date(), self.player.user.username,
        self.get_status_display())


class Event(models.Model):
    when = models.DateTimeField(_("Event datetime"))
    participants = models.ManyToManyField(UserSocialAuth, through=Participant)
    rounds = models.PositiveIntegerField(_("No of rounds"), default=2)

    class Meta:
        ordering = ('when',)

    def __unicode__(self):
        return u"Event: %s" % self.when

    @property
    def players_count(self):
        return len(self.participant_set.filter(status__in=['com', 'yes']))

    @property
    def commanders_count(self):
        return len(self.participant_set.filter(status__in=['com']))

    @property
    def fav_maps(self):
        cnt = EventMap.objects.filter(event=self,
                                      participant__status__in=['com', 'yes']). \
            values('map__name'). \
            annotate(Count('map')).order_by('-map__count')

        return cnt

    @property
    def players(self):
        return self.participant_set.filter(status__in=['com', 'yes']).order_by('status')


class Map(models.Model):
    name = models.CharField(_("Name of the map"), max_length=20)

    def __unicode__(self):
        return self.name


class UserSocialAuthProxy(UserSocialAuth):
    class Meta:
        proxy = True
        verbose_name = _("Steam login")

    def __unicode__(self):
        return self.user.username

