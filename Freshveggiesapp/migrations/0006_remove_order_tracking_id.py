# Generated by Django 5.1.2 on 2025-02-11 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swachathapp', '0005_alter_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tracking_id',
        ),
    ]
