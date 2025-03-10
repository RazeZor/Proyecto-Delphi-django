# Generated by Django 5.1.4 on 2025-01-21 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0025_clinico_esadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formularioclinico',
            name='AlcoholPreocupacion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='DrogasPreocupacion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='ansioso',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='deprimido',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='marihuanaPreocupacion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='nicotinaPreocupacion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='placer_cosas',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='preocupacion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='proposito',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formularioclinico',
            name='red_de_apoyo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
