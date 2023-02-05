import pandas as pd
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from recommender.api.serializers import RecommendationSerializer
from recommender.recommender_model.RecommenderSystem import Updater, MemoryBased
from transmit.models import MusicState, SensorState, Session
from recommender.utilities import OnMemoryCSVConvertor

from io import StringIO
from django.shortcuts import get_object_or_404


class RecommendMusic(generics.GenericAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        mb = MemoryBased()
        if serializer.is_valid():
            session_id = serializer.data.get("session_id")
            first_sequence_id = serializer.data.get("first_sequence")
            last_sequence_id = serializer.data.get("last_sequence")
            current_recommend_id = serializer.data.get("recommendation_id")

            current_session = get_object_or_404(Session, id=session_id)
            
            # check if it's the first request of the session
            if (first_sequence_id == 0) and (last_sequence_id == 0):
                recommended_music = mb.first_recommend(session_id=current_session.id,
                                                    user_id=current_session.user.id)
                return Response({"recommended_music": recommended_music})
                
            # check to ignore requests that they've had delay
            if current_recommend_id <= current_session.last_recommend_id:
                return Response(data={"error": f"the delayed id in the sequence"},
                                status=status.HTTP_400_BAD_REQUEST)

            else:
                current_session.last_recommend_id = current_recommend_id
                current_session.save(update_fields=["last_recommend_id"])

                music_records = MusicState.objects.filter(session=session_id).\
                    filter(sequence__gte=first_sequence_id).\
                    filter(sequence__lte=last_sequence_id).order_by("sequence")

                sensor_records = SensorState.objects.filter(session=session_id).\
                    filter(sequence__gte=first_sequence_id).\
                    filter(sequence__lte=last_sequence_id).order_by("sequence")

                print("sensor_records : ", sensor_records.count())

                # check if query is empty
                if sensor_records and music_records:
                    csv_OM_converter = OnMemoryCSVConvertor()
                    music_csv_file = csv_OM_converter.convert(
                        query_set=music_records)

                    sensor_csv_file = csv_OM_converter.convert(
                        query_set=sensor_records)

                    music_df = pd.read_csv(StringIO(music_csv_file))
                    sensor_df = pd.read_csv(StringIO(sensor_csv_file))
                    
                    updater = Updater()
                    updater.fit(music_df, sensor_df)

                    recommended_music = mb.recommend(user_id=current_session.user.id,
                                                    session_id=current_session.id)

                    return Response({"recommended_music": recommended_music})
                else:
                    return Response(data={"error": "empty query"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
