# Generated by Django 4.1.9 on 2023-05-30 10:31

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gponmap', '0003_alter_point_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='QgisPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'db_table': 'lines_all',
                'managed': False,
            },
        ),
    ]