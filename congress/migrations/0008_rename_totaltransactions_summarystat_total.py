# Generated by Django 3.2.6 on 2022-01-18 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0007_auto_20220118_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summarystat',
            old_name='totalTransactions',
            new_name='total',
        ),
    ]
