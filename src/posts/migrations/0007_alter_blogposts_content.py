# Generated by Django 4.2.4 on 2023-09-05 04:39

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_photo_blogposts_alter_blogposts_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogposts',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenu'),
        ),
    ]
