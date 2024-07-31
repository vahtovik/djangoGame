import csv
from django.http import HttpResponse

from .models import PlayerLevel, LevelPrize


class CSVExportService:
    @staticmethod
    def export_to_csv():
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="player_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])

        # Параметры пагинации
        chunk_size = 10000  # Размер чанка данных
        offset = 0

        while True:
            # Получаем кусок данных для PlayerLevel
            player_levels = PlayerLevel.objects.select_related('level').all()[offset:offset + chunk_size]
            if not player_levels:
                break

            # Получаем все призы для уровней в текущем чанке
            level_ids = player_levels.values_list('level_id', flat=True)
            level_prizes = LevelPrize.objects.filter(level_id__in=level_ids).select_related('prize')

            # Организуем призы по уровням
            level_prizes_dict = {}
            for prize in level_prizes:
                if prize.level_id not in level_prizes_dict:
                    level_prizes_dict[prize.level_id] = []
                level_prizes_dict[prize.level_id].append(f'{prize.prize.title}')

            # Записываем данные в CSV
            for player_level in player_levels:
                prizes = ', '.join(level_prizes_dict.get(player_level.level_id, []))
                writer.writerow([
                    player_level.player_id,
                    player_level.level.title,
                    player_level.is_completed,
                    prizes if player_level.is_completed else ''
                ])

            # Переходим к следующему чанку
            offset += chunk_size

        return response

# Без оптимизации
# class CSVExportService:
#     @staticmethod
#     def export_to_csv():
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="player_data.csv"'
#
#         writer = csv.writer(response)
#         writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])
#
#         player_levels = PlayerLevel.objects.select_related('player', 'level').all()
#         level_prizes = LevelPrize.objects.select_related('prize').all()
#
#         for player_level in player_levels:
#             prizes = level_prizes.filter(level=player_level.level)
#             prize_titles = ', '.join(prize.prize.title for prize in prizes)
#
#             writer.writerow([
#                 player_level.player.id,
#                 player_level.level.title,
#                 player_level.is_completed,
#                 prize_titles if player_level.is_completed else ''
#             ])
#
#         return response
