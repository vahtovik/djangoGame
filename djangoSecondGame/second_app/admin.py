from django.contrib import admin
from .models import Player, Level, Prize, PlayerLevel, LevelPrize, PlayerPrize


class PlayerLevelAdmin(admin.ModelAdmin):
    list_display = ('player', 'level', 'is_completed')
    list_filter = ('player', 'level', 'is_completed')


class LevelPrizeAdmin(admin.ModelAdmin):
    list_display = ('level', 'prize', 'received')
    list_filter = ('level', 'prize', 'received')


class PlayerPrizeAdmin(admin.ModelAdmin):
    list_display = ('player', 'prize', 'quantity')
    list_filter = ('player', 'prize', 'quantity')


admin.site.register(Player)
admin.site.register(Level)
admin.site.register(Prize)
admin.site.register(PlayerLevel, PlayerLevelAdmin)
admin.site.register(LevelPrize, LevelPrizeAdmin)
admin.site.register(PlayerPrize, PlayerPrizeAdmin)
