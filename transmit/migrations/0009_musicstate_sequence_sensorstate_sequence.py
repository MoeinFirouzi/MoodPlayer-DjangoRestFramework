# Generated by Django 4.1.1 on 2022-09-21 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transmit', '0008_auto_20220903_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicstate',
            name='sequence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorstate',
            name='sequence',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
