# Generated by Django 3.0.8 on 2020-08-09 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200809_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='problems',
            name='device_brand',
            field=models.CharField(blank=True, choices=[('T', 'Teckno'), ('S', 'Samsung'), ('U', 'Huawei'), ('O', 'Oppo')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='problems',
            name='device_type',
            field=models.CharField(blank=True, choices=[('A', 'Android'), ('I', 'Ios')], max_length=200, null=True),
        ),
    ]
