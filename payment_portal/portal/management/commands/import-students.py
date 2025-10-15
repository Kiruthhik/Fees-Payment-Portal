import csv
import random
from django.core.management.base import BaseCommand
from portal.models import Student

class Command(BaseCommand):
    help = "Import students from Entra ID exported CSV file into the Student model"

    def handle(self, *args, **options):
        # --- EDIT THIS PATH ---
        csv_file = r"C:\Users\HP\Documents\clg notes\sem7\cloud\project\payment_portal\portal\management\commands\exportUsers_2025-10-10.csv"

        # Distributions
        residence_choices = ["day_scholar", "hosteller"]
        admission_choices = ["counselling", "management"]

        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_rows = []

        with open(csv_file, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):  # start=2 to skip header row number
                try:
                    entra_oid = row.get("id") or row.get("Id") or row.get("ID")
                    email = (row.get("userPrincipalName") or "").strip().lower()
                    display_name = (row.get("displayName") or "").strip()

                    if not entra_oid or not email:
                        raise ValueError("Missing Entra OID or email")

                    # Split name into first and last
                    name_parts = display_name.split(" ", 1)
                    first_name = name_parts[0]
                    last_name = name_parts[1] if len(name_parts) > 1 else ""

                    enrolment_no = email.split("@")[0]

                    residence_type = random.choices(residence_choices, weights=[70, 30])[0]
                    admission_type = random.choices(admission_choices, weights=[50, 50])[0]
                    is_nri = random.choices([False, True], weights=[90, 10])[0]

                    # Try updating existing or creating new
                    student, created = Student.objects.update_or_create(
                        email=email,
                        defaults={
                            "entra_oid": entra_oid,
                            "first_name": first_name,
                            "last_name": last_name,
                            "enrolment_no": enrolment_no,
                            "residence_type": residence_type,
                            "admission_type": admission_type,
                            "is_nri": is_nri,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    skipped_count += 1
                    error_rows.append((i, str(e)))
                    continue

        self.stdout.write(self.style.SUCCESS("✅ Import Summary"))
        self.stdout.write(self.style.SUCCESS(f"  ✔️ Created records: {created_count}"))
        self.stdout.write(self.style.SUCCESS(f"  🔁 Updated records: {updated_count}"))
        self.stdout.write(self.style.WARNING(f"  ⚠️ Skipped records: {skipped_count}"))

        if error_rows:
            self.stdout.write(self.style.ERROR("\n❌ Errors encountered:"))
            for row_num, err in error_rows:
                self.stdout.write(f"  Row {row_num}: {err}")
