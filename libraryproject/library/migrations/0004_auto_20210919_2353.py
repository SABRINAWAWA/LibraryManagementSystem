# Generated by Django 3.2.7 on 2021-09-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20210919_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookitems',
            name='author',
        ),
        migrations.RemoveField(
            model_name='bookitems',
            name='bookID',
        ),
        migrations.RemoveField(
            model_name='bookitems',
            name='language',
        ),
        migrations.AddField(
            model_name='bookitems',
            name='authors',
            field=models.CharField(default='NoAuthor', max_length=200, verbose_name='authors'),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='average_rating',
            field=models.FloatField(default=0.0, verbose_name='average rating'),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='isbn13',
            field=models.CharField(default='000000000', max_length=50, unique=True, verbose_name='isbn 13'),
        ),
        migrations.AddField(
            model_name='bookitems',
            name='language_code',
            field=models.CharField(default='eng', max_length=50, verbose_name='language code'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='isbn',
            field=models.CharField(default='000000000', max_length=50, unique=True, verbose_name='isbn'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='num_pages',
            field=models.IntegerField(default=0, verbose_name='number of pages'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='publication_date',
            field=models.DateField(auto_now=True, max_length=50, verbose_name='publication date'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='publisher',
            field=models.CharField(default='NoPublisher', max_length=100, verbose_name='publisher'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='ratings_count',
            field=models.BigIntegerField(default=0, verbose_name='rating count'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='text_reviews_count',
            field=models.IntegerField(default=0, verbose_name='text review count'),
        ),
        migrations.AlterField(
            model_name='bookitems',
            name='title',
            field=models.CharField(default='NoTitle', max_length=255, verbose_name='title'),
        ),
    ]
