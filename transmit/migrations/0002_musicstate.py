# Generated by Django 3.2 on 2022-08-20 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transmit", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MusicState",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_time", models.DateTimeField(blank=True, null=True)),
                ("muted", models.BooleanField(blank=True, null=True)),
                ("position", models.CharField(blank=True, max_length=250, null=True)),
                ("state", models.CharField(blank=True, max_length=250, null=True)),
                ("volume", models.IntegerField(blank=True, null=True)),
                ("playlist_count", models.IntegerField(blank=True, null=True)),
                ("repeatMode", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "shuffle_mode",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("media_type", models.CharField(blank=True, max_length=250, null=True)),
                ("music_id", models.IntegerField(blank=True, null=True)),
                ("album", models.CharField(blank=True, max_length=250, null=True)),
                ("artist", models.CharField(blank=True, max_length=250, null=True)),
                ("duration", models.CharField(blank=True, max_length=250, null=True)),
                ("genre", models.CharField(blank=True, max_length=250, null=True)),
                ("energy", models.CharField(blank=True, max_length=250, null=True)),
                ("valence", models.CharField(blank=True, max_length=250, null=True)),
                ("title", models.CharField(blank=True, max_length=250, null=True)),
                ("year", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "session_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="transmit.session",
                    ),
                ),
            ],
        ),
    ]
