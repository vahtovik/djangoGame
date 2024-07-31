from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Player, Level
from .services import CSVExportService


class CompleteLevelView(APIView):
    def post(self, request, player_id, level_id):
        player = get_object_or_404(Player, id=player_id)
        level = get_object_or_404(Level, id=level_id)

        success, message = player.complete_level(level)

        if success:
            return Response({'detail': message}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)


def export_to_csv_view(request):
    return CSVExportService.export_to_csv()
