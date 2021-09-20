# Generated by Django 3.2.7 on 2021-09-20 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20210919_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookitems',
            name='language',
            field=models.CharField(default='eng', max_length=50),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='num_pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='publication_date',
            field=models.CharField(default='01-01-1900', max_length=50),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='publisher',
            field=models.CharField(default='NoPublisher', max_length=100),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='ratings_count',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='text_reviews_count',
            field=models.IntegerField(default=0),
        ),
    ]