# Generated by Django 3.0 on 2020-08-11 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200811_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
