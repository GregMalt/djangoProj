# Generated by Django 4.2.7 on 2023-11-28 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_item_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['category', 'name']},
        ),
    ]
