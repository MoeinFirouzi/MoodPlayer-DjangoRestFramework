# Generated by Django 4.1.1 on 2023-02-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transmit', '0009_musicstate_sequence_sensorstate_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='last_recommend_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]