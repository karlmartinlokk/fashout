# Generated by Django 5.0.1 on 2024-05-07 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rename_date_comment_raw_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='profile_image',
        ),
    ]
