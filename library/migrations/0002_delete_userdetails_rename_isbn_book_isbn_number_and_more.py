# Generated by Django 5.0 on 2025-03-22 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDetails',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='isbn',
            new_name='isbn_number',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default='No description provided.', max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
