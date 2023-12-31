# Generated by Django 4.1.7 on 2023-06-13 13:58

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gponmap', '0009_colorline'),
    ]

    operations = [
        migrations.CreateModel(
            name='QgisCoupling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('coupling', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'couplings_all',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='colorline',
            table='colorlines_all',
        ),
    ]
