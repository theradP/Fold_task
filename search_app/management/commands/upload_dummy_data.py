from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Users, Hashtags, Projects

fake = Faker()


class Command(BaseCommand):
    help = 'Populate dummy data for testing'

    def handle(self, *args, **kwargs):
        # Create fake users
        for _ in range(10):
            Users.objects.create(name=fake.name())

        # Create fake hashtags
        for _ in range(5):
            Hashtags.objects.create(name=fake.word())

        # Create fake projects
        for _ in range(20):
            project = Projects.objects.create(
                name=fake.catch_phrase(),
                slug=fake.slug(),
                description=fake.paragraph(),
            )

            # Add random hashtags to the project
            hashtags = Hashtags.objects.order_by("?")[:3]
            users = Users.objects.order_by("?")[:3]

            project.hashtags.set(hashtags)
            project.users.set(users)

        self.stdout.write(self.style.SUCCESS('Fake data populated successfully!'))



