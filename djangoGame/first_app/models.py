from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Player(models.Model):
    """
    Модель для представления игрока, связанного с пользователем Django.
    Хранит информацию о никнейме игрока и количестве очков-дейликов.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    nickname = models.CharField(max_length=20, default='player')
    daily_points = models.IntegerField(default=0)

    def __str__(self):
        return self.nickname

    def get_daily_bonus(self) -> tuple[bool, str]:
        """Проверяет, является ли сегодняшний день новым для начисления бонуса и, если да, начисляет его."""
        if self.is_new_day():
            self.daily_points += 1
            self.save()
            self.user.last_login = timezone.now()
            self.user.save()
            return True, 'Daily bonus awarded.'

        return False, 'Daily bonus already claimed.'

    def is_new_day(self) -> bool:
        """Определяет, является ли сегодняшний день новым днем входа пользователя."""
        if self.user.last_login is None:
            return True
        last_login_date = self.user.last_login.date()
        return last_login_date < timezone.now().date()

    def complete_level(self, level: 'Level') -> tuple[bool, str]:
        """
        Отмечает уровень как завершенный для игрока, если он еще не завершен.
        Начисляет вознаграждения за уровень.
        """
        player_level, created = PlayerLevel.objects.get_or_create(player=self, level=level)
        if player_level.is_completed:
            return False, 'Level already completed.'

        player_level.is_completed = True
        player_level.save()

        self.get_reward_for_level(level)
        return True, 'Level completed and rewards granted.'

    def get_reward_for_level(self, level: 'Level') -> None:
        """
        Начисляет вознаграждения игроку за завершение уровня.
        """
        level_rewards = LevelReward.objects.filter(level=level)
        for level_reward in level_rewards:
            boost_type = level_reward.reward
            player_boost, created = PlayerBoost.objects.get_or_create(
                player=self,
                boost=boost_type,
                defaults={'quantity': level_reward.quantity}
            )
            if not created:
                player_boost.quantity += level_reward.quantity
                player_boost.save()


class Boost(models.Model):
    """
    Модель для представления буста.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    """
    Модель для представления уровня в игре.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlayerLevel(models.Model):
    """
    Модель для представления связи между игроком и уровнем.
    Хранит информацию о том, завершил ли игрок уровень.
    """
    player = models.ForeignKey(Player, related_name='player_levels', on_delete=models.CASCADE)
    level = models.ForeignKey(Level, related_name='player_levels', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Level: "{self.level.name}", player: "{self.player.nickname}"'

    class Meta:
        unique_together = ('player', 'level')


class LevelReward(models.Model):
    """
    Модель для представления вознаграждений за уровень.
    """
    level = models.ForeignKey(Level, related_name='level_reward', on_delete=models.CASCADE)
    reward = models.ForeignKey(Boost, related_name='level_reward', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Level: "{self.level.name}", reward: "{self.reward.name}", quantity: "{self.quantity}"'


class PlayerBoost(models.Model):
    """
    Модель для представления бустов игрока.
    """
    player = models.ForeignKey(Player, related_name='player_boosts', on_delete=models.CASCADE)
    boost = models.ForeignKey(Boost, related_name='player_boosts', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('player', 'boost')

    def __str__(self):
        return f'Player: "{self.player.nickname}", boost: "{self.boost}", quantity: "{self.quantity}"'
