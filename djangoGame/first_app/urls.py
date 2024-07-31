from django.urls import path
from .views import PlayerListView, LevelListView, BoostListView, GetDailyBonusView, CompleteLevelView

app_name = 'first_app'
urlpatterns = [
    path('api/players/', PlayerListView.as_view(), name='player_list'),
    path('api/boosts/', BoostListView.as_view(), name='boost_list'),
    path('api/levels/', LevelListView.as_view(), name='level_list'),
    path('api/player/<int:player_id>/get_daily_bonus/', GetDailyBonusView.as_view(), name='get_daily_bonus'),
    path('api/player/<int:player_id>/complete_level/<int:level_id>/', CompleteLevelView.as_view(),
         name='complete_level'),
]
