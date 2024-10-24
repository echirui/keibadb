# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Jockey, Horse, Race, RaceResult


class RaceResultModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """テストデータの準備"""
        cls.jockey = Jockey.objects.create(name="武豊")
        cls.horse = Horse.objects.create(
            horse_key="1234567890", name="テスト馬", sex="牡"
        )
        RaceResult.objects.create(
            race_id="202410240101",
            horse_key=cls.horse.horse_key,
            jockey=cls.jockey,
            horse_number=1,
            running_time="1:23.4",
            odds=2.5,
            passing_order="1-1-1-1",
            finish_position=1,
            handicap=55.0,
            popularity=1,
        )
        RaceResult.objects.create(
            race_id="202410240102",
            horse_key=cls.horse.horse_key,
            jockey=cls.jockey,
            horse_number=2,
            running_time="1:24.5",
            odds=3.0,
            passing_order="2-2-2-2",
            finish_position=2,
            handicap=55.0,
            popularity=2,
        )
        RaceResult.objects.create(
            race_id="202410240103",
            horse_key=cls.horse.horse_key,
            jockey=cls.jockey,
            horse_number=3,
            running_time="1:25.6",
            odds=3.5,
            passing_order="3-3-3-3",
            finish_position=4,
            handicap=55.0,
            popularity=3,
        )

    def test_summarize_race_by_horse_key(self):
        """summarize_race_by_horse_keyメソッドのテスト"""
        summary = RaceResult.summarize_race_by_horse_key(horse_key="1234567890")
        self.assertEqual(summary["total_races"], 3)
        self.assertEqual(summary["finish_position_counts"]["1"], 1)
        self.assertEqual(summary["finish_position_counts"]["2"], 1)
        self.assertEqual(summary["finish_position_counts"]["3"], 0)
        self.assertEqual(summary["finish_position_counts"]["others"], 1)

    def test_summarize_race_by_horse_key_with_jockey(self):
        """騎手IDを指定したsummarize_race_by_horse_keyメソッドのテスト"""
        summary = RaceResult.summarize_race_by_horse_key(
            horse_key="1234567890", jockey_id=self.jockey.id
        )
        self.assertEqual(summary["total_races"], 3)
        self.assertEqual(summary["finish_position_counts"]["1"], 1)
        self.assertEqual(summary["finish_position_counts"]["2"], 1)
        self.assertEqual(summary["finish_position_counts"]["3"], 0)
        self.assertEqual(summary["finish_position_counts"]["others"], 1)


class HorseViewSetTest(APITestCase):
    def setUp(self):
        """テストデータの準備"""
        self.horse = Horse.objects.create(
            horse_key="1234567890", name="テスト馬", sex="牡"
        )

    def test_list_horses(self):
        """馬一覧取得APIのテスト"""
        url = reverse("horse-list")  # 'horse-list' は HorseViewSet の URL 名
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["horse_key"], "1234567890")

    def test_retrieve_horse(self):
        """馬詳細取得APIのテスト"""
        url = reverse("horse-detail", args=[self.horse.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["horse_key"], "1234567890")


class JockeyViewSetTest(APITestCase):
    # HorseViewSetTest と同様に JockeyViewSet のテストケースを作成
    pass


class RaceViewSetTest(APITestCase):
    def setUp(self):
        """テストデータの準備"""
        self.jockey = Jockey.objects.create(name="武豊")
        self.horse = Horse.objects.create(
            horse_key="1234567890", name="テスト馬", sex="牡"
        )
        self.race = Race.objects.create(
            race_id="202410240101",
            horse=self.horse,
            horse_key=self.horse.horse_key,
            jockey=self.jockey,
            horse_number=1,
            running_time="1:23.4",
            odds=2.5,
            passing_order="1-1-1-1",
            finish_position=1,
            weight=500,
            weight_change=0,
            sex="牡",
            age=3,
            handicap=55.0,
            final_600m_time=35.5,
            popularity=1,
            race_name="テストレース",
            date="2024-10-24",
            details="テスト詳細",
            debut=False,
            race_class="G1",
            surface="芝",
            distance=2000,
            direction="右",
            track_condition="良",
            weather="晴",
            start_at="15:40",
            venue_code="01",
            venue="東京",
            lap="0",
            pace="S",
            training_center="美浦",
            owner="テストオーナー",
            farm="テストファーム",
        )

    def test_list_races(self):
        """レース一覧取得APIのテスト"""
        url = reverse("race-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["race_id"], "202410240101")

    def test_filter_races_by_race_id(self):
        """レースIDで絞り込みAPIのテスト"""
        url = reverse("race-list") + "?race_id=20241024"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["race_id"], "202410240101")

    def test_filter_races_by_invalid_race_id(self):
        """無効なレースIDで絞り込みAPIのテスト"""
        url = reverse("race-list") + "?race_id=invalid"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
