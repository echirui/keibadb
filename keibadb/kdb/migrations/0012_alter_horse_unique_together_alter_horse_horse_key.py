# Generated by Django 5.1 on 2024-09-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdb', '0011_alter_horse_horse_key'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='horse',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='horse',
            name='horse_key',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]