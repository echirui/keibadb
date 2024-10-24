from rest_framework.serializers import ModelSerializer, SerializerMethodField
from kdb.models import Horse, Jockey, Race


class HorseSerializer(ModelSerializer):
    class Meta:
        model = Horse
        fields = "__all__"


class JockeySerializer(ModelSerializer):
    class Meta:
        model = Jockey
        fields = "__all__"


class RaceSerializer(ModelSerializer):
    jockey = SerializerMethodField()
    horse = SerializerMethodField()

    class Meta:
        model = Race
        fields = [
            "race_id",
            "horse_key",
            "horse_number",
            "running_time",
            "odds",
            "passing_order",
            "finish_position",
            "weight",
            "weight_change",
            "sex",
            "age",
            "handicap",
            "final_600m_time",
            "popularity",
            "race_name",
            "date",
            "details",
            "debut",
            "race_class",
            "surface",
            "distance",
            "direction",
            "track_condition",
            "weather",
            "start_at",
            "venue_code",
            "venue",
            "lap",
            "pace",
            "training_center",
            "owner",
            "farm",
            "horse",
            "jockey",
        ]

    def get_horse(self, obj):
        return HorseSerializer(Horse.objects.get(id=obj.horse_id)).data

    def get_jockey(self, obj):
        return JockeySerializer(Jockey.objects.get(id=obj.jockey_id)).data
