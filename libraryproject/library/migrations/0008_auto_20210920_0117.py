# Generated by Django 3.2.7 on 2021-09-20 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20210920_0100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookitems',
            options={'ordering': ('title', 'authors', 'average_rating', 'isbn', 'isbn13', 'language_code', 'num_pages', 'ratings_count', 'text_reviews_count', 'publication_date', 'publisher')},
        ),
        migrations.RemoveField(
            model_name='bookitems',
            name='bookID',
        ),
    ]
