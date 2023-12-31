# Generated by Django 4.2.2 on 2023-07-02 15:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MaxLengthValidator(30, message='Too many letters'), django.core.validators.RegexValidator('^[A-Za-z]+$', 'The text should contain only letters.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=40, null=True, validators=[django.core.validators.MaxLengthValidator(40, message='Too many letters'), django.core.validators.RegexValidator('^[A-Za-z]+$', 'The text should contain only letters.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.MaxLengthValidator(12, message='Have too many digits'), django.core.validators.RegexValidator('^\\d+$', 'The phone number should only contain digits.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MaxLengthValidator(30, message='Too many letters'), django.core.validators.RegexValidator('^[A-Za-z]+$', 'The text should contain only letters.')]),
        ),
    ]
