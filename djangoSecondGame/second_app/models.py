from django.db import models
from django.utils import timezone


class Player(models.Model):
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname

    def complete_level(self, level: 'Level') -> tuple[bool, str]:
        """
        Отмечает уровень как завершенный для игрока, если он еще не завершен.
        Начисляет вознаграждения за уровень.
        """
        player_level, created = PlayerLevel.objects.get_or_create(
            player=self,
            level=level,
            completed=timezone.now()
        )
        if player_level.is_completed:
            return False, 'Level already completed.'

        player_level.is_completed = True
        player_level.save()

        self.get_prize_for_level(level)
        return True, 'Level completed and prizes granted.'

    def get_reward_for_level(self, level: 'Level') -> None:
        """
        Начисляет вознаграждения игроку за завершение уровня.
        """
        level_prizes = LevelPrize.objects.filter(level=level)
        for level_prize in level_prizes:
            prize = level_prize.prize
            player_prize, created = PlayerPrize.objects.get_or_create(
                player=self,
                prize=prize,
                defaults={'quantity': 1}
            )
            if not created:
                player_prize.quantity += 1
                player_prize.save()


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Prize(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Level: "{self.level.title}", player: "{self.player.nickname}"'


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()

    def __str__(self):
        return f'Level: "{self.level.title}", prize: "{self.prize.title}"'


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, related_name='player_prize', on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, related_name='player_prize', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('player', 'prize')

    def __str__(self):
        return f'Player: "{self.player.nickname}", prize: "{self.prize.title}", quantity: "{self.quantity}"'
