from django.contrib import admin
from .models import SummonerV4, MatchparticipantV4, MatchlistV4, MatchteamV4

# Register your models here.
admin.site.register(SummonerV4)
admin.site.register(MatchparticipantV4)
admin.site.register(MatchlistV4)
admin.site.register(MatchteamV4)