# Generated by Django 3.1.4 on 2021-01-08 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='hash',
            field=models.CharField(max_length=10, verbose_name='Hash'),
        ),
        migrations.AlterField(
            model_name='link',
            name='initial_url',
            field=models.TextField(verbose_name='URL'),
        ),
    ]
