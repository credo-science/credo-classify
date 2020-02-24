# Generated by Django 3.0.3 on 2020-02-23 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ping',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.CredoUser'),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.CredoUser'),
        ),
        migrations.AddField(
            model_name='detection',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Device'),
        ),
        migrations.AddField(
            model_name='detection',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Team'),
        ),
        migrations.AddField(
            model_name='detection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.CredoUser'),
        ),
    ]