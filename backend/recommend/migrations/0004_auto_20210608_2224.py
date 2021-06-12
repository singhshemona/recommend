# Generated by Django 3.1.5 on 2021-06-08 22:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0003_booksdisplayed_goodreadsimport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksdisplayed',
            name='pages',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='booksdisplayed',
            name='publish_date',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='booksdisplayed',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), default=list, null=True, size=20),
        ),
    ]
