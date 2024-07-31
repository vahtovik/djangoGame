from django.contrib import admin
from .models import Player, Boost, Level, PlayerLevel, LevelReward, PlayerBoost


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'daily_points')


class PlayerLevelAdmin(admin.ModelAdmin):
    list_display = ('player', 'level', 'is_completed')
    list_filter = ('is_completed',)


class LevelRewardAdmin(admin.ModelAdmin):
    list_display = ('level', 'reward', 'quantity')
    list_filter = ('level', 'reward')


class PlayerBoostAdmin(admin.ModelAdmin):
    list_display = ('player', 'boost', 'quantity')
    list_filter = ('boost',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Boost)
admin.site.register(Level)
admin.site.register(PlayerLevel, PlayerLevelAdmin)
admin.site.register(LevelReward, LevelRewardAdmin)
admin.site.register(PlayerBoost, PlayerBoostAdmin)
