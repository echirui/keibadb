from rest_framework.viewsets import ModelViewSet


from kdb.models import Horse, Jockey, Race  # type: ignore
from kdb.serializers import HorseSerializer, JockeySerializer, RaceSerializer  # type: ignore


class HorseViewSet(ModelViewSet):
    """
    HorseModel
    """

    queryset = Horse.objects.all()
    serializer_class = HorseSerializer

    def get_queryset(self):
        """
        queryset
        """
        horse_id = self.request.query_params.get("horse_id", None)
        return Race.objects.filter(horse_id=horse_id).all()


class JockeyViewSet(ModelViewSet):
    """
    JockeyModel
    """

    queryset = Jockey.objects.all()
    serializer_class = JockeySerializer


class RaceViewSet(ModelViewSet):
    """
    RaceModel
    """

    queryset = Race.objects.all()
    serializer_class = RaceSerializer

    def get_queryset(self):
        """
        queryset
        """
        race_id = self.request.query_params.get("race_id", None)
        q = self.queryset
        return q.filter(race_id__startswith=race_id) if race_id else q
