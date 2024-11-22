# Generated by Django 4.2.16 on 2024-11-21 21:35

import bookshelf.book.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_book_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(help_text='Not more than 2000 characters and first letter should be upper or in Book an allowed quotation symbol.', validators=[django.core.validators.MaxLengthValidator(2000), bookshelf.book.validators.UpperValueValidator()]),
        ),
    ]