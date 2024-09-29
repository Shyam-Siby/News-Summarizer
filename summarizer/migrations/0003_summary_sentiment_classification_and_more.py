# Generated by Django 5.0.6 on 2024-09-28 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarizer', '0002_auto_20180712_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='sentiment_classification',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='sentiment_plot',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='sentiment_polarity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='sentiment_subjectivity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='summary',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='summary',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
