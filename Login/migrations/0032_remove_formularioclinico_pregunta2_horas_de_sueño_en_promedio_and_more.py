# Generated by Django 5.1.5 on 2025-01-31 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0031_paciente_profesion_paciente_trabajo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formularioclinico',
            name='pregunta2_horas_de_sueño_en_promedio',
        ),
        migrations.AddField(
            model_name='formularioclinico',
            name='despertares',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formularioclinico',
            name='hora_acostarse',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formularioclinico',
            name='hora_despertar',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formularioclinico',
            name='hora_levantarse',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formularioclinico',
            name='tiempo_dormirse',
            field=models.TextField(blank=True, null=True),
        ),
    ]
