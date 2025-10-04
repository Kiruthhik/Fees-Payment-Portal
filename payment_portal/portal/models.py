from django.db import models

class Student(models.Model):
    RESIDENCE = (('day_scholar', 'Day Scholar'), ('hosteller', 'Hosteller'))
    ADMISSION = (('counselling', 'Counselling'), ('management', 'Management'))

    enrolment_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    entra_oid = models.CharField(max_length=100, unique=True)  # Azure AD object id
    residence_type = models.CharField(max_length=20, choices=RESIDENCE)
    admission_type = models.CharField(max_length=20, choices=ADMISSION)
    is_nri = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.enrolment_no or 'no-enrol'})"

class FeeConfig(models.Model):   # optional, for editable amounts
    key_name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.key_name} = {self.amount}"
