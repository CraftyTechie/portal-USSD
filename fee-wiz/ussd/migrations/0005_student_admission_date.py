# Generated by Django 5.0.1 on 2024-03-06 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0004_alter_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admission_date',
            field=models.DateField(auto_now=True),
        ),
    ]
