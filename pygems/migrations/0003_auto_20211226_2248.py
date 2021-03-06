# Generated by Django 3.2.5 on 2021-12-26 16:48

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('pygems', '0002_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=tinymce.models.HTMLField(max_length=200),
        ),
    ]
