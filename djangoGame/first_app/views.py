from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Player, Level, PlayerLevel, LevelReward, PlayerBoost, Boost
from .serializers import PlayerSerializer, LevelSerializer, BoostSerializer


class GetDailyBonusView(APIView):
    def post(self, request, player_id):
        player = get_object_or_404(Player, id=player_id)

        success, message = player.get_daily_bonus()

        if success:
            return Response({'detail': message}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)


class CompleteLevelView(APIView):
    def post(self, request, player_id, level_id):
        player = get_object_or_404(Player, id=player_id)
        level = get_object_or_404(Level, id=level_id)

        success, message = player.complete_level(level)

        if success:
            return Response({'detail': message}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)


class PlayerListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class LevelListView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class BoostListView(generics.ListAPIView):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer
