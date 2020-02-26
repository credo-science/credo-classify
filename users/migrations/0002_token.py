from django.db import migrations

from users.models import User, Token


def post_migrations(arg1, arg2):
    from credo_classification.settings import INIT_ADMIN_USER
    u = User.objects.filter(username=INIT_ADMIN_USER).first()  # type: User
    Token.objects.create(key='0000000000000000000000000000000000000000', user=u)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(post_migrations),
    ]
