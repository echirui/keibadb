# Generated by Django 5.1 on 2024-09-19 22:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Horse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horse_key', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Jockey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.CharField(max_length=12)),
                ('horse_key', models.CharField(max_length=10)),
                ('horse_number', models.IntegerField()),
                ('running_time', models.CharField(max_length=255)),
                ('odds', models.FloatField()),
                ('passing_order', models.CharField(max_length=255)),
                ('finish_position', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('weight_change', models.IntegerField()),
                ('sex', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('handicap', models.FloatField()),
                ('final_600m_time', models.FloatField()),
                ('popularity', models.IntegerField()),
                ('race_name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('details', models.TextField()),
                ('debut', models.BooleanField(default=False)),
                ('race_class', models.CharField(max_length=255)),
                ('surface', models.CharField(max_length=255)),
                ('distance', models.IntegerField()),
                ('direction', models.CharField(max_length=255)),
                ('track_condition', models.CharField(max_length=255)),
                ('weather', models.CharField(max_length=255)),
                ('venue_code', models.CharField(max_length=255)),
                ('venue', models.CharField(max_length=255)),
                ('lap', models.CharField(max_length=255)),
                ('pace', models.CharField(max_length=255)),
                ('training_center', models.CharField(max_length=4)),
                ('owner', models.CharField(max_length=255)),
                ('farm', models.CharField(max_length=255)),
                ('horse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kdb.horse')),
                ('jockey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kdb.jockey')),
            ],
            options={
                'unique_together': {('race_id', 'horse_number')},
            },
        ),
    ]