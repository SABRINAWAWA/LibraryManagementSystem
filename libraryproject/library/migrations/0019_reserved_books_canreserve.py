# Generated by Django 3.2.7 on 2021-10-21 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_rented_books_latereturn'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserved_books',
            name='canReserve',
            field=models.BooleanField(default=False, verbose_name='Can Reserve'),
        ),
    ]