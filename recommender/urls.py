from django.urls import path
from recommender.api.views import RecommendMusic

urlpatterns = [
    path("recommend/", RecommendMusic.as_view(), name="recommend_music"),
]
