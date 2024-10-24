# -*- coding: utf8 -*-

from django.db.models import (
    Model,
    CharField,
    BooleanField,
    TextField,
    IntegerField,
    FloatField,
    DateField,
    ForeignKey,
    CASCADE,
    Case,
    When,
    Count,
)


# Create your models here.
class Jockey(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Horse(Model):
    horse_key = CharField(max_length=10, unique=True)
    name = CharField(max_length=255)
    birth_year = CharField(max_length=12, null=True, blank=True)
    sex = CharField(max_length=255, null=True, blank=True)
    coat_color = CharField(max_length=255, null=True, blank=True)
    father_key = CharField(max_length=10, null=True, blank=True)
    mother_key = CharField(max_length=10, null=True, blank=True)
    race_result = CharField(max_length=255, null=True, blank=True)
    race_text = CharField(max_length=255, null=True, blank=True)
    relatives = CharField(max_length=255, null=True, blank=True)
    prize = CharField(max_length=255, null=True, blank=True)
    is_stallion = BooleanField(default=False, null=True, blank=True)
    trainer_name = CharField(max_length=255, null=True, blank=True)
    trainer_key = CharField(max_length=7, null=True, blank=True)
    training_center = CharField(max_length=5, null=True, blank=True)
    owner_name = CharField(max_length=255, null=True, blank=True)
    owner_key = CharField(max_length=8, null=True, blank=True)
    farm_name = CharField(max_length=255, null=True, blank=True)
    farm_key = CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.sex})"


class Race(Model):
    class Meta:
        unique_together = (("race_id", "horse_number"),)
        ordering = ["horse_number"]

    race_id = CharField(max_length=12)
    horse = ForeignKey(Horse, on_delete=CASCADE)
    horse_key = CharField(max_length=10)
    jockey = ForeignKey(Jockey, on_delete=CASCADE)
    horse_number = IntegerField()
    running_time = CharField(max_length=255)
    odds = FloatField()
    passing_order = CharField(max_length=255)
    finish_position = IntegerField()
    weight = IntegerField(blank=True, null=True)
    weight_change = IntegerField(blank=True, null=True)
    sex = CharField(max_length=255)
    age = IntegerField()
    handicap = FloatField()
    final_600m_time = FloatField(blank=True, null=True)
    popularity = IntegerField()
    race_name = CharField(max_length=255)
    date = DateField()
    details = TextField()
    debut = BooleanField(default=False)
    race_class = CharField(max_length=255)
    surface = CharField(max_length=255)
    distance = IntegerField()
    direction = CharField(max_length=255)
    track_condition = CharField(max_length=255)
    weather = CharField(max_length=255)
    start_at = CharField(max_length=255, blank=True)
    venue_code = CharField(max_length=255)
    venue = CharField(max_length=255)
    lap = CharField(max_length=255)
    pace = CharField(max_length=255)
    training_center = CharField(max_length=4)
    owner = CharField(max_length=255)
    farm = CharField(max_length=255)

    def __str__(self):
        return f"Race {self.race_id} - {self.horse.name} - {self.jockey.name}"


class RaceResult(Model):
    class Meta:
        unique_together = (("race_id", "horse_number"),)

    race_id = CharField(max_length=12)
    horse_key = CharField(max_length=10)
    jockey = ForeignKey(Jockey, on_delete=CASCADE)
    horse_number = IntegerField()
    running_time = CharField(max_length=255)
    odds = FloatField()
    passing_order = CharField(max_length=255)
    finish_position = IntegerField()
    weight = IntegerField(blank=True, null=True)
    weight_change = IntegerField(blank=True, null=True)
    handicap = FloatField()
    final_600m_time = FloatField(blank=True, null=True)
    popularity = IntegerField()

    def summarize_race_by_horse_key(horse_key, jockey_id=None):
        """Summarizes Race data for a given horse_key.

        Args:
          horse_key: The horse_key to filter by.

        Returns:
          A dictionary containing the summarized data, including:
          - total_races: The total number of races for the horse.
          - finish_position_counts: A dictionary containing the counts of each
            finish position (1, 2, 3, and others).
        """
        races = RaceResult.objects.filter(horse_key=horse_key)
        if jockey_id:
            races = races.filter(jockey_id=jockey_id)

        total_races = races.count()

        finish_position_counts = (
            races.annotate(
                finish_position_group=Case(
                    When(finish_position=1, then=1),
                    When(finish_position=2, then=2),
                    When(finish_position=3, then=3),
                    default=4,
                    output_field=IntegerField(),
                )
            )
            .values("finish_position_group")
            .annotate(count=Count("finish_position_group"))
        )

        finish_position_counts_dict = {
            "1": 0,
            "2": 0,
            "3": 0,
            "others": 0,
        }
        for item in finish_position_counts:
            position = str(item["finish_position_group"])
            count = item["count"]
            if position in finish_position_counts_dict:
                finish_position_counts_dict[position] = count
            else:
                finish_position_counts_dict["others"] = count

        return {
            "total_races": total_races,
            "finish_position_counts": finish_position_counts_dict,
        }

    def __str__(self):
        return f"RaceResult{self.race_id}-{self.horse_key}-{self.horse_number}"
