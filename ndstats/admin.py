from django.contrib import admin
from ndstats.models import Server, Player, PlayerIP, Match, MatchPlayer, Chatlog, FoodProduct


@admin.register(FoodProduct)
class FoodProductAdmin(admin.ModelAdmin):
    fields = ('name', 'price', 'weight', 'is_available',  'description', 'picture')
    list_display = ('name', 'price', 'weight', 'is_available',)


class PlayersInline(admin.TabularInline):
    model = MatchPlayer
    fields = ('player',)
    readonly_fields = ('player',)
    extra = 0


class ChatInline(admin.TabularInline):
    model = Chatlog
    fields = ('timestamp', 'player', 'message')
    readonly_fields = ('timestamp', 'player', 'message')
    extra = 0


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = ('nick',)


@admin.register(PlayerIP)
class PlayerIPAdmin(admin.ModelAdmin):
    search_fields = ('ip', 'player__nick')
    list_display = ('player', 'when', 'ip')


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass


@admin.register(MatchPlayer)
class MatchPlayerAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'player', 'timestamp_last_change')
    list_select_related = ('match', 'player')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'map', 'started', 'finished',)
    list_select_related = ('server',)
    list_filter = ('server',)

    inlines = [PlayersInline, ChatInline]


@admin.register(Chatlog)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('player', 'message', 'timestamp')
    search_fields = ('player', 'message',)
