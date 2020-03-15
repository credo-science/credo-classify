from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

from definitions.models import Attribute
from users.models import User, Token


class Command(BaseCommand):
    help = 'Create and initialize admin user and init build-in attributes'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', help='admin user name')
        parser.add_argument('-p', '--password', help='admin user password')
        parser.add_argument('-e', '--email', help='admin user e-mail', default='')
        parser.add_argument('-t', '--token', help='generate token for admin user with UUID "000..."', action="store_true")

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        if not username or not password:
            print('Invalid parameters\n--username and --password are required')
            return

        u = User.objects.create_user(username, email, password)  # type: User
        u.is_superuser = True
        u.is_staff = True
        u.save()

        Attribute.objects.create(name='accuracy', description='GPS accuaracy', author=u, kind='b', active=True)
        Attribute.objects.create(name='latitude', description='GPS latitude', author=u, kind='b', active=True)
        Attribute.objects.create(name='longitude', description='GPS longitude', author=u, kind='b', active=True)
        Attribute.objects.create(name='altitude', description='GPS altitude', author=u, kind='b', active=True)
        Attribute.objects.create(name='height', description='Height of image frame', author=u, kind='b', active=True)
        Attribute.objects.create(name='width', description='Width of image frame', author=u, kind='b', active=True)
        Attribute.objects.create(name='x', description='X on image of center of crop', author=u, kind='b', active=True)
        Attribute.objects.create(name='y', description='Y on image of center of crop', author=u, kind='b', active=True)
        Attribute.objects.create(name='spot', description='Spot-like hit', kind='cs', author=u, active=True)
        Attribute.objects.create(name='worm', description='Worm-like hit', kind='cs', author=u, active=True)
        Attribute.objects.create(name='track', description='Track-like hit', kind='cs', author=u, active=True)
        Attribute.objects.create(name='artifact', description='Artifact (fake hit: hot pixel, damage of CMOS/CCD, deliberate fraud)', kind='cs', author=u, active=True)
        Attribute.objects.create(name='class', description='One arbitrary class: 1 - spot, 2 - worm, 3 - track, 4 - artifact, n - future defined', kind='co', author=u, active=True)

        if options['token']:
            Token.objects.create(key='0000000000000000000000000000000000000000', user=u)
