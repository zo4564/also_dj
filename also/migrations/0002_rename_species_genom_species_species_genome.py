# Generated by Django 5.0.6 on 2024-06-04 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('also', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='species',
            old_name='species_genom',
            new_name='species_genome',
        ),
    ]
