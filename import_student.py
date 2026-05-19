import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoginLogout.settings')
django.setup()

from logger.models import LearnerProfile

def import_csv():
    with open('student.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            LearnerProfile.objects.get_or_create(
                id_number=row['id_number'],
                full_name=row['full_name']
            )
    print("Successfully imported all student!")

if __name__ == "__main__":
    import_csv()