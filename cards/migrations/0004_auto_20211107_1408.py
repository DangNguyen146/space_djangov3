# Generated by Django 3.1.13 on 2021-11-07 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20211107_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emails',
            old_name='descriptione',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='emails',
            old_name='namee',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='phones',
            old_name='descriptionp',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='phones',
            old_name='namep',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='socials',
            old_name='descriptions',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='socials',
            old_name='images',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='socials',
            old_name='names',
            new_name='name',
        ),
    ]
