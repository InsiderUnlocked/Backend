# Generated by Django 3.2.3 on 2022-01-24 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0015_auto_20220123_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='company',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='industry',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='sector',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]