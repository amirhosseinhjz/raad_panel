from django.core.management.base import BaseCommand
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Duplicates BlogPost records for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('post_id', type=int, help='ID of the BlogPost to duplicate')
        parser.add_argument('count', type=int, help='Number of times to duplicate the BlogPost')

    def handle(self, *args, **kwargs):
        post_id = kwargs['post_id']
        count = kwargs['count']

        try:
            original_post = BlogPost.objects.get(pk=post_id)
        except BlogPost.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"BlogPost with ID {post_id} does not exist."))
            return

        for _ in range(count):
            original_post.pk = None  # Create a new instance
            original_post.save()

        self.stdout.write(self.style.SUCCESS(f"{count} copies of BlogPost {post_id} have been created."))
