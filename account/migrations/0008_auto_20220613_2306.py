# Generated by Django 3.1.6 on 2022-06-13 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20220613_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='matric_no',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
