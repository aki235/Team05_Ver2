import json
from django.core.management.base import BaseCommand
from myapp.models import Subject

class Command(BaseCommand):
    help = 'JSONファイルから科目をデータベースにロードします'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='科目が含まれているJSONファイル')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for subject_data in data['subject']:
            subject_number = subject_data[0]
            name = subject_data[1]

            subject, created = Subject.objects.get_or_create(
                subject_number=subject_number,
                defaults={'name': name},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created subject: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Subject already exists: {name}'))
