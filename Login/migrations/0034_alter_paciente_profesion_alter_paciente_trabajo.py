# Generated by Django 5.1.5 on 2025-02-02 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0033_alter_paciente_profesion_alter_paciente_trabajo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='profesion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='trabajo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
