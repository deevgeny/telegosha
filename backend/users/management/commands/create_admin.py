from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):
    """Custom command to create admin user (superuser)."""

    def add_arguments(self, parser):
        parser.add_argument('--username', nargs='?', type=str)
        parser.add_argument('--email', nargs='?', type=str)
        parser.add_argument('--password', nargs='?', type=str)

    def handle(self, *args, **options):
        required_args = ['username', 'email', 'password']
        missing = False
        for i in required_args:
            if options[i] is None:
                missing = True
                self.stdout.write(
                    self.style.WARNING(
                        ('WARNING: Option %s is required' % i)
                    )
                )
        if missing:
            return
        if User.objects.filter(username=options['username']).exists():
            self.stdout.write(
                self.style.WARNING(
                    ('WARNING: Admin with "%s" username already exists'
                     % options['username'])
                )
            )
            return
        try:
            User.objects.create_user(
                username=options['username'],
                email=options['email'],
                password=options['password'],
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS('SUCCESS: Admin user created')
            )
        except BaseException:
            raise CommandError('Unexpected error happened')
