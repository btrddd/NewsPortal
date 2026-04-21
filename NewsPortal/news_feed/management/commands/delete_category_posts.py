from django.core.management.base import BaseCommand


from news_feed.models import Post, Category


class Command(BaseCommand):
    help = (
        'Command deletes all posts in the specified categories.\n'
        'Arguments must contain values ​​of the "category_name" field '
        'from the "Category" table.'
    )

    missing_args_message = 'Not enough arguments.'


    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write(
            'Are you sure you want to delete all posts from categories '
            f'{', '.join(f'"{category}"' for category in options['category'])}?'
        )

        answer = input('Type "yes" to continue: ')

        if answer == 'yes':
            self.stdout.write(str(options['category']))
            for category in options['category']:
                try:
                    category_obj = Category.objects.get(category_name=category)
                    Post.objects.filter(category=category_obj).delete()
                    self.stdout.write(self.style.SUCCESS(f'All posts in the "{category}" category have been deleted.'))
                except Category.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Category "{category}" does not exist.'))
        else:
            self.stdout.write('Command canceled.')
        