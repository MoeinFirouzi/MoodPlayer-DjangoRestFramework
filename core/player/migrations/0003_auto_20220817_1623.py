# Generated by Django 3.2 on 2022-08-17 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_auto_20220817_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_image',
            field=models.ImageField(blank=True, null=True, upload_to='album/images/'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='artist_image',
            field=models.ImageField(blank=True, null=True, upload_to='artist/images/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='address',
            field=models.FileField(blank=True, null=True, upload_to='music/files/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='musics', to='player.album'),
        ),
        migrations.AlterField(
            model_name='music',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='musics', to='player.artist'),
        ),
        migrations.AlterField(
            model_name='music',
            name='energy',
            field=models.CharField(blank=True, choices=[('Too Negative', 'Too Negative'), ('Negative', 'Negative'), ('Neutral', 'Neutral'), ('Positive', 'Positive'), ('Too Positive', 'Too Positive')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='genre',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='song_image',
            field=models.ImageField(blank=True, null=True, upload_to='music/images/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='valence',
            field=models.CharField(blank=True, choices=[('Too Negative', 'Too Negative'), ('Negative', 'Negative'), ('Neutral', 'Neutral'), ('Positive', 'Positive'), ('Too Positive', 'Too Positive')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
