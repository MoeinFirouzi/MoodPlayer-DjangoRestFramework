from rest_framework import serializers
from ..models import Music, Album, Artist
from core.settings import PORT, BASE_URL

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):

    absolute_url = serializers.SerializerMethodField()

    artist = serializers.CharField()
    artist_id = serializers.ReadOnlyField(source="get_artist_id")
    artist_image = serializers.FileField(required=False)

    # Refers to "get_artist_absolute_url" in Music Model
    artist_url = serializers.ReadOnlyField(source="get_artist_absolute_url")

    # Refers to "get_artist_absolute_url" in MusicSerializer
    artist_absolute_url = serializers.SerializerMethodField()

    album = serializers.CharField()
    album_id = serializers.ReadOnlyField(source="get_album_id")
    album_image = serializers.FileField(required=False)

    # Refers to "get_album_absolute_url" in Music Model
    album_url = serializers.ReadOnlyField(source="get_album_absolute_url")

    # Refers to "get_album_absolute_url" in MusicSerializer
    album_absolute_url = serializers.SerializerMethodField()
    
    address = serializers.SerializerMethodField()
    song_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Music
        fields = "__all__"

    def get_absolute_url(self, obj):
        """
        Returns Music instance absolute url
        """
        request = self.context.get("request")
        if request:
            obj_url = obj.get_absolute_url()
            base_url = BASE_URL
            port = PORT
            if port:
                base_url = f"{base_url}:{port}"
            return f"http://{base_url}{obj_url}"
        else:
            return None

    def get_album_absolute_url(self, obj):
        """
        Returns related album to music instance absolute url
        """
        request = self.context.get("request")
        if request:
            obj_url = obj.album.get_absolute_url()
            base_url = BASE_URL
            port = PORT
            if port:
                base_url = f"{base_url}:{port}"
            return f"http://{base_url}{obj_url}"
        else:
            return None

    def get_artist_absolute_url(self, obj):
        """
        Returns related artist to music instance absolute url
        """
        request = self.context.get("request")
        if request:
            obj_url = obj.artist.get_absolute_url()
            base_url = BASE_URL
            port = PORT
            if port:
                base_url = f"{base_url}:{port}"
            return f"http://{base_url}{obj_url}"
        else:
            return None

    def get_address(self, obj):
        obj_url = obj.address.path
        base_url = BASE_URL
        port = PORT
        if port:
            base_url = f"{base_url}:{port}"
            
        return f"http://{base_url}{obj_url}"
        
        
    def get_song_image(self, obj):
        obj_url = obj.song_image.path
        base_url = BASE_URL
        port = PORT
        if port:
            base_url = f"{base_url}:{port}"
            
        return f"http://{base_url}{obj_url}"
        
        
    def create(self, validated_data):
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
