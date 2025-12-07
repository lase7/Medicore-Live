# patients/management/commands/seed_patients.py
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from patients.models import PatientRecord

class Command(BaseCommand):
    help = 'Populates the database with dummy patient data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Patient Data...")

        # Lists for random generation
        first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Tochukwu", "Chioma", "Emeka", "Amaka"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Okonkwo", "Eze", "Adeyemi", "Bello"]
        conditions = ["Hypertension", "Type 2 Diabetes", "Asthma", "None", "Migraine", "Arthritis", "None", "None", "Bronchitis"]
        allergies = ["Penicillin", "Peanuts", "Latex", "None", "None", "Shellfish", "Dust Mites"]
        blood_types = ['A+', 'O+', 'B-', 'AB+', 'O-']

        records = []
        for _ in range(50):
            # Generate Random DOB (between 18 and 80 years ago)
            start_date = date.today() - timedelta(days=80*365)
            random_days = random.randint(0, 62 * 365)
            dob = start_date + timedelta(days=random_days)

            p = PatientRecord(
                full_name=f"{random.choice(first_names)} {random.choice(last_names)}",
                date_of_birth=dob,
                blood_type=random.choice(blood_types),
                allergies=random.choice(allergies),
                existing_conditions=random.choice(conditions),
                emergency_contact_name=f"{random.choice(first_names)} {random.choice(last_names)}",
                emergency_contact_phone=f"555-{random.randint(1000,9999)}"
            )
            records.append(p)

        # Bulk Create (Much faster than saving one by one)
        PatientRecord.objects.bulk_create(records)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(records)} dummy patients!"))