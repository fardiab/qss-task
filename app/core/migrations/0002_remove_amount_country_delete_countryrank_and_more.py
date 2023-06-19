# Generated by Django 4.2.2 on 2023-06-15 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amount',
            name='country',
        ),
        migrations.DeleteModel(
            name='CountryRank',
        ),
        migrations.RemoveField(
            model_name='rank',
            name='country',
        ),
        migrations.RemoveField(
            model_name='year',
            name='indicator',
        ),
        migrations.AddField(
            model_name='country',
            name='amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='rank',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Amount',
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
    ]