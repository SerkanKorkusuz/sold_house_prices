from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser non-interactively if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument('--username', help='Username of the superuser')
        parser.add_argument('--email', help='Email of the superuser')
        parser.add_argument('--password', help='Password of the superuser')

    def handle(self, *args, **kwargs):
        user = get_user_model()
        if not user.objects.filter(username=kwargs['username']).exists():
            user.objects.create_superuser(username=kwargs['username'],
                                          email=kwargs['email'],
                                          password=kwargs['password'])
