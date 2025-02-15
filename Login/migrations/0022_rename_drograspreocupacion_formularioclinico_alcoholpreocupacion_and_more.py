# Generated by Django 5.1.4 on 2025-01-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0021_alter_formularioclinico_medicamento_efectivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formularioclinico',
            old_name='DrograsPreocupacion',
            new_name='AlcoholPreocupacion',
        ),
        migrations.RenameField(
            model_name='formularioclinico',
            old_name='cigarroPreocupacion',
            new_name='DrogasPreocupacion',
        ),
        migrations.RenameField(
            model_name='formularioclinico',
            old_name='condicioncigarro',
            new_name='condicionAlcohol',
        ),
        migrations.RemoveField(
            model_name='formularioclinico',
            name='cigarroSiOno',
        ),
        migrations.AddField(
            model_name='formularioclinico',
            name='AlcoholSiOno',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='NicotinaSiOno',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='drogasSiOno',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='marihuanaSiOno',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
