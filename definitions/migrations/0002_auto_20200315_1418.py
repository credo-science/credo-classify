# Generated by Django 3.0.4 on 2020-03-15 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('definitions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='relation',
            name='dest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relation_dest', to='definitions.Attribute'),
        ),
        migrations.AddField(
            model_name='relation',
            name='src',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relation_src', to='definitions.Attribute'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together={('src', 'dest')},
        ),
    ]