# Generated by Django 2.2.3 on 2019-07-23 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_deck_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deck',
            options={'permissions': (('can_edit', 'Can edit'),)},
        ),
    ]
