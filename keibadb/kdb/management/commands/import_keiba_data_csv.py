import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from kdb.models import Jockey, Horse, Race  # type: ignore


class Command(BaseCommand):
    help = "ファイルをインポートするコマンド"

    def add_arguments(self, parser):
        parser.add_argument(
            "--datafile", type=str, help="インポートするファイルのパス", required=True
        )
        parser.add_argument("--skip", type=int, default=0, help="スキップする行数")

    def handle(self, *args, **options):
        datafile_path = options["datafile"]
        skip_rows = options["skip"]

        if not datafile_path:
            self.stdout.write(self.style.ERROR("ファイルパスが指定されていません"))
            return

        try:
            print(f"import_csv: {datafile_path}")
            self.import_csv(datafile_path, skip_rows)

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"ファイルが見つかりません: {datafile_path}")
            )

    def import_csv(self, file_path, skip):
        set_race_id = Race.objects.values_list("race_id", flat=True)
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if int(row[0]) < skip:
                    continue
                if row[0] in set_race_id:
                    continue

                horse_name = row[1]
                horse_key = row[2]
                jockey_name = row[3]

                # Jockeyを取得または作成
                jockey, _ = Jockey.objects.get_or_create(name=jockey_name)

                # Horseを取得または作成
                horse, created = Horse.objects.get_or_create(
                    name=horse_name, horse_key=horse_key
                )

                # 199005010702,ダイシンプロミス,1987104789,関口睦介,4,1:27.6,15.1,3-2,2,442,-12,牝,4,53,51.8,6,4歳未勝利,1990年2月17日,1回東京7日目,4歳未勝利,ダ,1400,左,不良,晴,10:25,05,東京,12.6-11.2-11.6-12.5-12.6-13.1-13.9,12.6-23.8-35.4-47.9-60.5-73.6-87.5 (12.6-12.6),東,高木嘉夫,高橋金次
                # Raceを作成
                race = Race(
                    race_id=row[0],
                    horse=horse,
                    horse_key=horse_key,
                    jockey=jockey,
                    horse_number=row[4],
                    running_time=row[5],
                    odds=row[6] if row[6] != "---" else 0,
                    passing_order=row[7],
                    finish_position=row[8].split("(")[0]
                    if row[8] not in ("中", "取", "失", "除", "降")
                    else 99,
                    weight=row[9] if row[9] else -1,
                    weight_change=row[10] if row[10] else 0,
                    sex=row[11],
                    age=row[12],
                    handicap=row[13],
                    final_600m_time=row[14] if row[14] else 9999,
                    popularity=row[15] if row[15] else -1,
                    race_name=row[16],
                    date=datetime.strptime(row[17], "%Y年%m月%d日"),
                    details=row[18],
                    debut=created,
                    race_class=row[19],
                    surface=row[20],
                    distance=row[21],
                    direction=row[22],
                    track_condition=row[23],
                    weather=row[24],
                    start_at=row[25],
                    venue_code=row[26],
                    venue=row[27],
                    lap=row[28],
                    pace=row[29],
                    training_center=row[30],
                    owner=row[31],
                    farm=row[32],
                )
                try:
                    race.save()
                except Exception as e:
                    print(*row)
                    print(e.__class__.__name__)  # ZeroDivisionError
                    print(e.args)  # ('division by zero',)
                    print(e)  # division by zero
                    print(f"{e.__class__.__name__}: {e}")
