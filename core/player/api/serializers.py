from dataclasses import fields
from rest_framework import serializers
from ..models import Music, Album, Artist


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class UploadMusicSerializer(serializers.ModelSerializer):
    artist = serializers.CharField()
    artist_image = serializers.FileField(required=False)

    album = serializers.CharField()
    album_image = serializers.FileField(required=False)

    class Meta:
        model = Music
        fields = '__all__'

    def create(self, validated_data):

        artist_instance, created = Artist.objects.get_or_create(
            name=validated_data['artist'])

        if created or validated_data.get('artist_image'):
            artist_instance.artist_image = validated_data.get('artist_image')
            artist_instance.save()

        album_instance, created = Album.objects.get_or_create(
            name=validated_data['album'])
        if created or validated_data.get('album_image'):
            album_instance.album_image = validated_data.get('album_image')
            album_instance.save()

        validated_data.pop('artist', None)
        validated_data.pop('album', None)
        validated_data.pop('artist_image', None)
        validated_data.pop('album_image', None)
        music_instance = Music.objects.create(**validated_data)
        music_instance.artist = artist_instance
        music_instance.album = album_instance
        music_instance.save()

        return music_instance


class MusicListSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    album  = AlbumSerializer()
    class Meta:
        model = Music
        fields = '__all__'