# Generated by Django 5.1.7 on 2025-04-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academic', '0007_alter_unit_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='result_grade',
            field=models.CharField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3'), (4, 'Year 4')], max_length=2),
        ),
    ]
