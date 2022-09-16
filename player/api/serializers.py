from rest_framework import serializers
from ..models import Music, Album, Artist
from core.settings import PORT, BASE_URL


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base_url = BASE_URL
        port = PORT
        if port:
            base_url = f"{base_url}:{port}"

        artist_image_url = instance.album_image.url
        representation['album_image'] = f"http://{base_url}{artist_image_url}"
        return representation


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base_url = BASE_URL
        port = PORT
        if port:
            base_url = f"{base_url}:{port}"

        artist_image_url = instance.artist_image.url
        representation['artist_image'] = f"http://{base_url}{artist_image_url}"
        return representation


class MusicSerializer(serializers.ModelSerializer):
    artist = serializers.CharField()
    artist_id = serializers.ReadOnlyField(source="get_artist_id")
    artist_image = serializers.FileField(required=False)

    # Refers to "get_artist_absolute_url" in Music Model
    artist_url = serializers.ReadOnlyField(source="get_artist_absolute_url")

    album = serializers.CharField()
    album_id = serializers.ReadOnlyField(source="get_album_id")
    album_image = serializers.FileField(required=False)

    # Refers to "get_album_absolute_url" in Music Model
    album_url = serializers.ReadOnlyField(source="get_album_absolute_url")

    class Meta:
        model = Music
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base_url = BASE_URL
        port = PORT
        if port:
            base_url = f"{base_url}:{port}"

        file_url = instance.address.url
        song_image_url = instance.song_image.url
        absolute_url = instance.get_absolute_url()
        album_absolute_url = instance.album.get_absolute_url()
        artist_absolute_url = instance.artist.get_absolute_url()

        representation['address'] = f"http://{base_url}{file_url}"
        representation['song_image'] = f"http://{base_url}{song_image_url}"
        representation['absolute_url'] = f"http://{base_url}{absolute_url}"
        representation['album_absolute_url'] = f"http://{base_url}{album_absolute_url}"
        representation['artist_absolute_url'] = f"http://{base_url}{artist_absolute_url}"

        return representation

    def create(self, validated_data):
        artist_instance, created = Artist.objects.get_or_create(
            name=validated_data["artist"].lower()
        )

        if created or validated_data.get("artist_image"):
            artist_instance.artist_image = validated_data.get("artist_image")
            artist_instance.save()

        album_instance, created = Album.objects.get_or_create(
            name=validated_data["album"].lower()
        )
        if created or validated_data.get("album_image"):
            album_instance.album_image = validated_data.get("album_image")
            album_instance.save()

        validated_data.pop("artist", None)
        validated_data.pop("album", None)
        validated_data.pop("artist_image", None)
        validated_data.pop("album_image", None)
        music_instance = Music.objects.create(**validated_data)
        music_instance.artist = artist_instance
        music_instance.album = album_instance
        music_instance.save()

        return music_instance

    def update(self, instance, validated_data):

        artist_instance, created = Artist.objects.get_or_create(
            name=validated_data["artist"]
        )

        if created or validated_data.get("artist_image"):
            artist_instance.artist_image = validated_data.get("artist_image")
            artist_instance.save()

        album_instance, created = Album.objects.get_or_create(
            name=validated_data["album"]
        )
        if created or validated_data.get("album_image"):
            album_instance.album_image = validated_data.get("album_image")
            album_instance.save()

        validated_data.pop("artist", None)
        validated_data.pop("album", None)
        validated_data.pop("artist_image", None)
        validated_data.pop("album_image", None)

        instance.artist = artist_instance
        instance.album = album_instance
        instance.save()

        return super().update(instance, validated_data)
