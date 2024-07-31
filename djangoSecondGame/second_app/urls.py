from django.urls import path
from second_app import views
from second_app.views import CompleteLevelView

app_name = 'second_app'
urlpatterns = [
    path('api/player/<int:player_id>/complete_level/<int:level_id>/', CompleteLevelView.as_view(),
         name='complete_level'),
    path('api/export_to_csv/', views.export_to_csv_view, name='export_to_csv'),
]
