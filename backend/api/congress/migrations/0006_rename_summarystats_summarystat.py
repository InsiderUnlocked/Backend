# Generated by Django 3.2.6 on 2022-01-18 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0005_summarystats'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SummaryStats',
            new_name='SummaryStat',
        ),
    ]
