# Generated by Django 5.1 on 2024-09-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdb', '0012_alter_horse_unique_together_alter_horse_horse_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horse',
            name='father',
        ),
        migrations.RemoveField(
            model_name='horse',
            name='mother',
        ),
        migrations.AddField(
            model_name='horse',
            name='father_key',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='horse',
            name='mother_key',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='horse',
            name='horse_key',
            field=models.CharField(max_length=10),
        ),
    ]
