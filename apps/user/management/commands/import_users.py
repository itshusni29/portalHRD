import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Import users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import users from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                # Remove BOM from the first header (username)
                if reader.fieldnames[0].startswith('\ufeff'):
                    reader.fieldnames[0] = reader.fieldnames[0].replace('\ufeff', '')

                for row in reader:
                    username = row['username']
                    first_name = row['first_name']
                    last_name = row['last_name']
                    email = row['email']
                    password = row['password']
                    role = row['role']
                    occupation = row['occupation']
                    department = row['department']
                    section = row['section']
                    cc = row['cc']

                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password,
                            role=role,
                            occupation=occupation,
                            department=department,
                            section=section,
                            cc=cc,
                        )
                        self.stdout.write(self.style.SUCCESS(f'User "{username}" created successfully!'))
                    else:
                        self.stdout.write(self.style.WARNING(f'User "{username}" already exists. Skipping.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{csv_file}" not found.'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in CSV file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('User import process completed.'))
