# Generated by Django 3.2.7 on 2021-10-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_auto_20211021_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented_books',
            name='lateReturn',
            field=models.BooleanField(default=False, verbose_name='Late Return'),
        ),
    ]
