# Generated by Django 5.1 on 2024-09-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdb', '0010_alter_horse_birth_year_alter_horse_horse_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horse',
            name='horse_key',
            field=models.CharField(max_length=10),
        ),
    ]
