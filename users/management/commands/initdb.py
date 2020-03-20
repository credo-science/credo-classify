from typing import Optional

from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

from definitions.models import Attribute
from users.models import User, Token


def create_attribute(*args, **kwargs):
    a = Attribute.objects.filter(name=kwargs['name']).count()
    if not a:
        Attribute.objects.create(**kwargs)
        print('Attribute %s created' % kwargs['name'])
    else:
        print('Attribute %s just exists' % kwargs['name'])


class Command(BaseCommand):
    help = 'Create and initialize admin user and init build-in attributes'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', help='admin user name', default='')
        parser.add_argument('-p', '--password', help='admin user password, when no provided then admin user will not be created', default='')
        parser.add_argument('-e', '--email', help='admin user e-mail', default='')
        parser.add_argument('-t', '--token', help='generate token for admin user with UUID "000..."', action="store_true")

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        u = None  # type: Optional[User]

        if username and password:
            u = User.objects.create_user(username, email, password)
            u.is_superuser = True
            u.is_staff = True
            u.save()

            if options['token']:
                Token.objects.create(key='0000000000000000000000000000000000000000', user=u)

        elif not username and not password:
            pass
        elif username:
            u = User.objects.filter(username=username).first()
            if u is None:
                print('Username is not created')
                return
        else:
            print('Invalid parameters\n--username and --password are required')
            return

        if u is not None:
            create_attribute(name='accuracy', description='GPS accuaracy', author=u, kind='b', active=True)
            create_attribute(name='latitude', description='GPS latitude', author=u, kind='b', active=True)
            create_attribute(name='longitude', description='GPS longitude', author=u, kind='b', active=True)
            create_attribute(name='altitude', description='GPS altitude', author=u, kind='b', active=True)
            create_attribute(name='height', description='Height of image frame', author=u, kind='b', active=True)
            create_attribute(name='width', description='Width of image frame', author=u, kind='b', active=True)
            create_attribute(name='x', description='X on image of center of crop', author=u, kind='b', active=True)
            create_attribute(name='y', description='Y on image of center of crop', author=u, kind='b', active=True)
            create_attribute(name='spot', description='Spot-like hit', kind='cs', author=u, active=True)
            create_attribute(name='worm', description='Worm-like hit', kind='cs', author=u, active=True)
            create_attribute(name='track', description='Track-like hit', kind='cs', author=u, active=True)
            create_attribute(name='multi', description='Multi hit', kind='cs', author=u, active=True)
            create_attribute(name='amazing', description='Amazing hit (not artifact but it amazing)', kind='cs', author=u, active=True)
            create_attribute(name='track', description='Track-like hit', kind='cs', author=u, active=True)
            create_attribute(name='artifact', description='Artifact (fake hit: hot pixel, damage of CMOS/CCD, deliberate fraud)', kind='cs', author=u, active=True)
            create_attribute(name='class', description='One arbitrary class: 1 - spot, 2 - worm, 3 - track, 4 - artifact, 5 - multi, 6 - amazing, n - future defined', kind='co', author=u, active=True)
