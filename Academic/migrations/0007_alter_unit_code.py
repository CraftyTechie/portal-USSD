# Generated by Django 5.1.7 on 2025-04-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academic', '0006_clearancerequest_delete_clearance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='code',
            field=models.CharField(choices=[('BIT 110', 'BIT 111'), ('BIT 123', 'BIT 117'), ('BIT 210', 'BIT 211'), ('BIT 213', 'BIT 227'), ('BIT 313', 'BIT 310'), ('BIT 311', 'BIT 322'), ('BIT 410', 'BIT 411'), ('BIT 423', 'BIT 424')], max_length=10),
        ),
    ]
