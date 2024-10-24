# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
import time
import csv
import sys
import re

from django.core.management.base import BaseCommand
from kdb.models import Jockey, Horse, Race


class Command(BaseCommand):
    help = 'ファイルをインポートするコマンド'

    def add_arguments(self, parser):
        parser.add_argument('--horse_id', type=str, help='horse_id', required=True)

    def handle(self, *args, **options):
        horse_id = options['horse_id']
        create_horse(horse_id)


def create_horse(horse_key, horse_name="",depth=0,is_stallion=False):
    if depth == 10:
        return
    if horse_key == "":
        return

    if Horse.objects.filter(horse_key=horse_key,is_stallion=True).exists():
        print("  "*depth + f"skip: {horse_key}")
        #horse = Horse.objects.get(horse_key=horse_key)
        #father_key,mother_key = horse.father_key, horse.mother_key
        #create_horse(horse_key=father_key,depth=depth+1,is_stallion=True)
        #create_horse(horse_key=mother_key,depth=depth+1,is_stallion=True)
        return

    url = f'https://db.netkeiba.com/horse/{horse_key}/'
    print("  "*depth + f"url = {url}")
    try:
        time.sleep(0.05)  # 10秒待機
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("  "*depth + f"Error: {e}")
        print("  "*depth + "Retrying in 10 seconds...")
        time.sleep(10)  # 10秒待機
        r = requests.get(url)

    soup = BeautifulSoup(r.content.decode("euc-jp", "ignore"), "html.parser")
    if not soup:
        return
    is_horse_attr = soup.select_one('p.txt_01')
    is_active = False
    sex = None
    coat_color = None
    if is_horse_attr:
        horse_attr = list(soup.select_one('p.txt_01').get_text().split('　'))
        is_active = horse_attr[0] == "現役"
        sex = horse_attr[1][0]
        coat_color = horse_attr[2].split(' ')[0]

    table = soup.select('.db_prof_table>tr>td')
    if not soup.select_one('.horse_title>h1'):
        return
    horse_name = soup.select_one('.horse_title>h1').get_text()

    blood = soup.select('table.blood_table>tr>td>a')
    father = blood[0]["href"].split("/")[3]
    father_name = None
    if father:
        father_name = blood[0].get_text()
    mother = blood[3]["href"].split("/")[3]
    mother_name = None
    if mother:
        mother_name = blood[3].get_text()
    birth_year = table[0].get_text()
    trainer_name = table[1].get_text().split('(')[0].strip()
    trainer_key = ''
    training_center = ''
    if table[1].select('a'):
        trainer_key = table[1].select('a')[0]['href'].split('/')[2]
        if table[1].get_text().count('('):
            training_center = table[1].get_text().split('(')[1][:-1]
    owner_name = table[2].get_text().strip()
    owner_key = ''
    if table[2].select('a'):
        owner_key = table[2].select('a')[0]['href'].split('/')[2]
    farm_name = table[-7].get_text().strip()
    farm_key = ''
    if table[-7].select('a'):
        farm_key = table[-7].select('a')[0]['href'].split('/')[2]
    prize = table[-4].get_text().strip()
    race_result = table[-3].get_text().split('[')[1][:-1]
    race_text = table[-2].get_text()
    relatives = ','.join([t['href'].split('/')[2] for t in table[-1].select('a')])

    print("  "*depth + f"horse_key={horse_key},father={father},father_name={father_name},mother={mother},mother_name={mother_name},trainer_name={trainer_name},traner_key={trainer_key},training_center={training_center},owner_name={owner_name},owner_key={owner_key},farm_name={farm_name},farm_key={farm_key}")

    create_horse(horse_key=father,depth=depth+1,is_stallion=True)
    create_horse(horse_key=mother,depth=depth+1,is_stallion=True)

    if Horse.objects.filter(horse_key=horse_key).exists():
        if is_active:
            print("  "*depth + "skip5")
            pass
        else:
            Horse.objects.filter(horse_key=horse_key).update(name=horse_name,birth_year=birth_year,race_result=race_result,race_text=race_text,father_key=father,mother_key=mother,relatives=relatives,coat_color=coat_color,sex=sex,is_stallion=is_stallion,trainer_name=trainer_name,trainer_key=trainer_key,training_center=training_center,owner_name=owner_name,owner_key=owner_key,prize=prize,farm_name=farm_name,farm_key=farm_key)
            print("  "*depth + "non-active-update!!!",horse_key,horse_name)
    else:
        Horse.objects.create(horse_key=horse_key,name=horse_name,birth_year=birth_year,race_result=race_result,race_text=race_text,father_key=father,mother_key=mother,relatives=relatives,coat_color=coat_color,sex=sex,is_stallion=is_stallion,trainer_name=trainer_name,trainer_key=trainer_key,training_center=training_center,owner_name=owner_name,owner_key=owner_key,prize=prize,farm_name=farm_name,farm_key=farm_key)
        print("  "*depth + "created!!",horse_key,horse_name)
    
    print("  "*depth + "end")


    #class Horse(models.Model):
    #    class Meta:
    #        unique_together = (('horse_key'),)
    #    horse_key = models.CharField(max_length=10,unique=True)
    #    name = models.CharField(max_length=255)
    #    birth_year = models.IntegerField(null=True, blank=True)
    #    sex = models.CharField(max_length=255,null=True,blank=True)
    #    coat_color = models.CharField(max_length=255,null=True,blank=True)
    #    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_father')
    #    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_mother')
    #    race_result = models.CharField(max_length=255,null=True,blank=True)
    #    race_text = models.CharField(max_length=255,null=True,blank=True)
    #    relatives = models.CharField(max_length=255,null=True,blank=True)
    #
    #    def __str__(self):
    #        return f"{self.name} ({self.sex})"
