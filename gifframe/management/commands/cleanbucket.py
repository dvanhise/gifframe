from django.core.management.base import BaseCommand
from gifframe.models import Frame
from gifframe.settings import MAIN_BUCKET, AWS_CONNECTION


class Command(BaseCommand):
    help = 'Deletes frames from s3 that aresn\'t being referenced anywhere in the database'

    def add_arguments(self, parser):
        parser.add_argument('--dryrun',
                            action='store_true',
                            default=False,
                            help='Make it a dry run, don\'t delete anything')

    def handle(self, *args, **options):
        conn = AWS_CONNECTION
        bucket = conn.get_bucket(MAIN_BUCKET, validate=False)
        if not bucket:
            self.stdout.write('<<error>> Couldn\'t connect to bucket ' + MAIN_BUCKET)
            return None

        count = 0
        allKeys = bucket.get_all_keys()
        self.stdout.write('<<log>> {} s3 keys found'.format(len(allKeys)))
        allFrames = Frame.objects.all().values_list('image', flat=True)
        for key in allKeys:
            if key.name not in allFrames:
                self.stdout.write('<<log>> Deleting key {}'.format(key.name))
                count += 1
                if not options['dryrun']:
                    key.delete()

        self.stdout.write('<<log>> {} s3 keys deleted'.format(count))
