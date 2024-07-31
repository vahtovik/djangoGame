from rest_framework import serializers
from .models import Player, Boost, Level, PlayerBoost, LevelReward


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class PlayerBoostSerializer(serializers.ModelSerializer):
    boost = BoostSerializer()

    class Meta:
        model = PlayerBoost
        fields = ['boost', 'quantity']


class LevelRewardSerializer(serializers.ModelSerializer):
    reward = BoostSerializer()

    class Meta:
        model = LevelReward
        fields = ['reward', 'quantity']
