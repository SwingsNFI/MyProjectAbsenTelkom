# Generated by Django 3.0.7 on 2020-06-09 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('absentelkom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_acara',
            name='keterangan_acara',
            field=models.CharField(default=None, max_length=400),
        ),
    ]
