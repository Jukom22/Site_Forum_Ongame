# Generated by Django 5.0.4 on 2024-04-24 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastro_usuario',
            name='senha',
            field=models.CharField(default='8a9bdbc14553980660e7c9b109b23bc03aff95394a6b790a8f62d9573a7ea4dc', max_length=256),
        ),
    ]