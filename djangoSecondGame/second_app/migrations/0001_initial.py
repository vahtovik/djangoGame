# Generated by Django 5.0.7 on 2024-07-31 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.DateField()),
                ('is_completed', models.BooleanField(default=False)),
                ('score', models.PositiveIntegerField(default=0)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_app.level')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_app.player')),
            ],
        ),
        migrations.CreateModel(
            name='LevelPrize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.DateField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_app.level')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_app.prize')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerPrize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_prize', to='second_app.player')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_prize', to='second_app.prize')),
            ],
            options={
                'unique_together': {('player', 'prize')},
            },
        ),
    ]
