from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.db.models import Sum
from django.utils.functional import cached_property
from valve.source.a2s import ServerQuerier
from valve.steam.id import SteamID

TEAM_SPEC = 0  # TODO - is it 0?
TEAM_CONS = 1
TEAM_EMP = 2

TEAM_CHOICES = (
    (TEAM_SPEC, 'UNASSIGNED'),
    (TEAM_CONS, 'CONSORTIUM'),
    (TEAM_EMP, 'EMPIRE'),
)

TEAM_CHOICES_REVERSE = {
    'SPECTATOR': TEAM_SPEC,
    'UNASSIGNED': TEAM_SPEC,
    'CONSORTIUM': TEAM_CONS,
    'EMPIRE': TEAM_EMP,
    '#ND_Team_Unassigned': TEAM_SPEC,
    '#ND_Spectate': TEAM_SPEC,
}

# this is switched, so when we get loser, lookup gets winner
TEAM_CHOICES_FLIPPED = {
    'CONSORTIUM': 'EMPIRE',
    'EMPIRE': 'CONSORTIUM',
}


class Error(models.Model):
    timestamp = models.DateTimeField()
    line = models.CharField(max_length=500)


class Server(models.Model):
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField()
    active = models.BooleanField(default=True)
    port = models.PositiveIntegerField(default=27015)
    map = models.CharField(max_length=32, blank=True)

    class Meta:
        unique_together = ('ip', 'port')

    @property
    def full_address(self):
        return (self.ip, self.port)

    def create_match(self, timestamp):
        return Match.objects.create(
            server=self,
            started=timestamp,
            map=self.map,
        )

    def get_unfinished(self):
        return Match.objects.filter(server=self, finished__isnull=True)

    def finish_all(self, timestamp):
        return self.get_unfinished().update(finished=timestamp)

    def get_absolute_url(self):
        return reverse('servers', args=[self.pk])

    @cached_property
    def remote_info(self):
        q = ServerQuerier(self.full_address)
        data = {}
        try:
            data['info'] = q.info()
            data['players'] = q.players()
        except Exception:
            pass

        return data

    def __str__(self):
        return self.name or self.full_address

    def set_map_name(self, map_name):
        self.map = map_name
        self.save(update_fields=['map'])


class Match(models.Model):
    server = models.ForeignKey(Server)
    map = models.CharField(max_length=20, null=True)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    winner = models.PositiveSmallIntegerField(choices=TEAM_CHOICES, null=True)

    class Meta:
        ordering = ['-started']
        verbose_name_plural = "Matches"

    def __str__(self):
        return "#%s since %s" % (self.id, self.started)

    def finish(self, timestamp):
        if not self.finished:
            self.finished = timestamp
            self.save(update_fields=['finished'])

    def start(self, timestamp):
        self.started = timestamp
        self.save(update_fields=['started'])

    def set_map_name(self, map_name):
        self.map = map_name
        self.save()

    def set_winner(self, winner):
        self.winner = TEAM_CHOICES_REVERSE[winner]
        self.save(update_fields=['winner'])

    def set_loser(self, loser):
        self.set_winner(TEAM_CHOICES_FLIPPED[loser])

    def finalize_players(self, timestamp):
        for player in self.matchplayer_set.filter(team_final__isnull=True):
            player.team_final = player.team_current
            player.update_team_time(timestamp, stop=True)
            player.update_commander_time(timestamp, stop=True)
            player.save()

        comms = {
            TEAM_EMP: self.matchplayer_set.exclude(time_empire_cmd=0). \
                order_by('-time_empire_cmd').first(),
            TEAM_CONS: self.matchplayer_set.exclude(time_consortium_cmd=0). \
                order_by('-time_consortium_cmd').first(),
        }
        for team, comm in comms.items():
            if comm:
                comm.commander = team
                comm.save(update_fields=['commander'])

    @cached_property
    def commanders(self):
        comm_emp = self.matchplayer_set.filter(time_empire_cmd__isnull=False, time_empire_cmd__gt=0).order_by(
            '-time_empire_cmd').first()
        comm_cons = self.matchplayer_set.filter(time_consortium_cmd__isnull=False, time_consortium_cmd__gt=0).order_by(
            '-time_consortium_cmd').first()

        return {
            TEAM_EMP: comm_emp,
            TEAM_CONS: comm_cons,
        }

    @property
    def players(self):
        if not self.finished:
            return {}
        return self.finished_results

    @cached_property
    def finished_results(self):
        data = {
            TEAM_EMP: [],
            TEAM_CONS: [],
        }
        for player in self.matchplayer_set.order_by('-score'):
            team = TEAM_EMP if player.time_empire > player.time_consortium else TEAM_CONS
            if self.commanders[team] == player:
                continue
            data[team].append(player)

        return data

    @property
    def duration(self):
        return self.finished - self.started

    def get_absolute_url(self):
        return reverse('match_detail', args=[self.pk])


class MatchPlayer(models.Model):
    player = models.ForeignKey('ndstats.Player')
    match = models.ForeignKey(Match)
    buildings = models.PositiveIntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    res_captured = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)

    team_final = models.PositiveSmallIntegerField(choices=TEAM_CHOICES,
                                                  null=True)
    team_current = models.PositiveSmallIntegerField(choices=TEAM_CHOICES,
                                                    null=True)

    timestamp_last_change = models.DateTimeField(null=True)
    time_empire = models.PositiveIntegerField(default=0)
    time_consortium = models.PositiveIntegerField(default=0)

    timestamp_cmd_change = models.DateTimeField(null=True)
    time_empire_cmd = models.PositiveIntegerField(default=0)
    time_consortium_cmd = models.PositiveIntegerField(default=0)
    commander = models.PositiveSmallIntegerField(choices=TEAM_CHOICES,
                                                 null=True)

    class Meta:
        unique_together = (
            ('player', 'match')
        )

    def __str__(self):
        return self.player.nick

    def disconnect(self, timestamp):
        self.update_commander_time(timestamp, stop=True)
        self.update_team_time(timestamp, stop=True)
        self.save()

    def stop_prev_commander(self, timestamp, new_comm):
        old_comm = MatchPlayer.objects.filter(
            match=new_comm.match, commander=new_comm.team_current). \
            exclude(pk=new_comm.pk)

        for comm in old_comm:
            comm.update_commander_time(timestamp)
            comm.commander = TEAM_SPEC
            comm.save()

    def promote_to_commander(self, timestamp):
        # there's not 'demote' signal
        self.stop_prev_commander(timestamp, self)

        self.timestamp_cmd_change = timestamp
        self.commander = self.team_current
        self.save(update_fields=['timestamp_cmd_change', 'commander'])

    def kill_structure(self):
        self.buildings += 1
        self.save(update_fields=['buildings'])

    def kill(self):
        self.kills += 1
        self.save(update_fields=['kills'])

    def died(self):
        self.deaths += 1
        self.save(update_fields=['deaths'])

    def suicide(self):
        self.kills -= 1
        self.deaths += 1
        self.save(update_fields=['kills', 'deaths'])

    def change_team(self, timestamp, team):
        """
        - on connected
        - on disconnected
        - weaponstats
        - changed role to (happens on first spawn)
        """
        new_team_id = TEAM_CHOICES_REVERSE[team]
        if new_team_id == self.team_current:
            return

        self.update_team_time(timestamp, save=False)
        self.team_current = new_team_id
        self.save()

    def update_score(self, score):
        self.score = score
        self.save(update_fields=['score'])

    def update_commander_time(self, timestamp, stop=False, save=False):
        if self.timestamp_cmd_change:
            diff = (timestamp - self.timestamp_cmd_change).total_seconds()
            diff = max(diff, 0)

            if self.commander == TEAM_EMP:
                self.time_empire_cmd += diff
            elif self.commander == TEAM_CONS:
                self.time_consortium_cmd += diff

        if stop and not self.match.finished:
            self.timestamp_cmd_change = None
            self.commander = None
        else:
            self.timestamp_cmd_change = timestamp

        if save:
            self.save()

    def update_team_time(self, timestamp, stop=False, save=False):
        if self.timestamp_last_change:
            diff = (timestamp - self.timestamp_last_change).total_seconds()
            diff = max(diff, 0)

            if self.team_current == TEAM_EMP:
                self.time_empire += diff
            elif self.team_current == TEAM_CONS:
                self.time_consortium += diff

        if stop and not self.match.finished:
            self.timestamp_last_change = None
            self.team_current = 0
        else:
            self.timestamp_last_change = timestamp

        if save:
            self.save()

    def captured(self):
        self.resource_captured += 1
        self.save(update_fields=['resource_captured'])


class MatchEvent(models.Model):
    EVENT_DEATH, EVENT_DESTROYED, EVENT_BUILT = (0, 1, 2)
    EVENT_CHOICES = (
        (EVENT_DEATH, 'death'),
        (EVENT_DESTROYED, 'destroyed'),
        (EVENT_BUILT, 'built'),
    )

    match = models.ForeignKey(Match)
    when = models.DateTimeField()
    what = models.IntegerField(choices=EVENT_CHOICES)
    team = models.PositiveSmallIntegerField(choices=TEAM_CHOICES)
    where_x = models.IntegerField()
    where_y = models.IntegerField()
    where_z = models.IntegerField()
    entity = models.IntegerField(blank=True, null=True)
    entype = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['when']


class Player(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    nick = models.CharField(max_length=64)
    nick_history = models.ManyToManyField('ndstats.PlayerNick',
                                          related_name='nick_history')
    ip_history = models.ManyToManyField('ndstats.PlayerIP',
                                        related_name='ip_history')
    clantag = models.CharField(max_length=32, null=True)
    score = models.BigIntegerField(default=0)
    score_saved = models.IntegerField(default=0)  # score saved until match ID
    avatar = models.URLField(null=True)

    def set_clantag(self, clantag):
        self.clantag = clantag or None
        self.save(update_fields=['clantag'])
        return True

    def save_ip(self, timestamp, ip):
        PlayerIP.objects.get_or_create(player=self, ip=ip,
                                       defaults={'when': timestamp})

    def set_nick(self, nick):
        self.nick = nick
        nick_history = PlayerNick.objects.create(
            player=self,
            nick=nick,
            changed=datetime.now())
        self.nick_history.add(nick_history)
        self.save(update_fields=['nick'])

    def __str__(self):
        return self.nick

    def get_absolute_url(self):
        return reverse('player_detail', kwargs={'pk': self.id})

    @cached_property
    def community_url(self):
        return SteamID.from_text(self.id).community_url()

    @cached_property
    def kills(self):
        return MatchPlayer.objects.filter(player=self).aggregate(sum_kills=Sum(F('kills')))['sum_kills']

    def avatar_full(self):
        return self.avatar.replace('.jpg', '_full.jpg')


class PlayerIP(models.Model):
    player = models.ForeignKey(Player)
    ip = models.GenericIPAddressField(db_index=True)
    when = models.DateTimeField()

    class Meta:
        unique_together = (
            ('player', 'ip'),
        )


class PlayerNick(models.Model):
    player = models.ForeignKey(Player)
    nick = models.CharField(max_length=64)
    changed = models.DateTimeField(auto_now_add=True)


class Chatlog(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
    timestamp = models.DateTimeField(db_index=True)
    message = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    team = models.PositiveSmallIntegerField(choices=TEAM_CHOICES, null=True)

    class Meta:
        ordering = ['-timestamp']


class UnknownLine(models.Model):
    ip_address = models.GenericIPAddressField()
    line = models.CharField(max_length=300)
