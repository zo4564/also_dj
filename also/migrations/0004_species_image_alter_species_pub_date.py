# Generated by Django 5.0.6 on 2024-06-06 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('also', '0003_species_pub_date_species_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='species_images/'),
        ),
        migrations.AlterField(
            model_name='species',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 6, 11, 29, 1, 167761), verbose_name='date published'),
        ),
    ]