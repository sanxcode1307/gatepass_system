from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    

    mobile = models.CharField(max_length=15)
    

    prn = models.CharField(max_length=50)

    # ---- Education Info ----
    EDUCATION_LEVEL_CHOICES = [
        ('School', 'School'),
        ('Polytechnic', 'Polytechnic'),
        ('Engineering', 'Engineering'),
        ('BPharmacy', 'BPharmacy'),
        ('DPharmacy', 'DPharmacy'),
    ]
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)

    YEAR_CHOICES = [
        ("FY", "First Year"),
        ("SY", "Second Year"),
        ("TY", "Third Year"),
        ("FoY", "Fourth Year"),
    ]

    SEM_CHOICES = [
        ("1", "Semester 1"),
        ("2", "Semester 2"),
        ("3", "Semester 3"),
        ("4", "Semester 4"),
        ("5", "Semester 5"),
        ("6", "Semester 6"),
        ("7", "Semester 7"),
        ("8", "Semester 8"),
    ]

    year = models.CharField(
        max_length=10,
        choices=YEAR_CHOICES,
        default="FY"
    )

    sem = models.CharField(
        max_length=10,
        choices=SEM_CHOICES,
        default="1"
    )

    department = models.CharField(max_length=100)
    hostel = models.CharField(max_length=50)

    room_no = models.CharField(max_length=10, null=True, blank=True)

    parent_name = models.CharField(max_length=100)
    parent_mobile = models.CharField(max_length=15)


      # 👇 NEW FIELD
    parent_email = models.EmailField()

    
    address = models.TextField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"





from django.db import models
from django.contrib.auth.models import User
import uuid

class Gatepass(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    room_no = models.CharField(max_length=10)

   
    reason = models.TextField()

    DEST_CHOICES = [
    ('HOME', 'Home'),
    ('LOCAL', 'Local'),
    ]

    destination = models.CharField(
        max_length=10,
        choices=DEST_CHOICES,
        default='HOME'
    )


    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('out', 'Out'),
            ('in', 'In'),
        ],
        default='pending'
    )


   

    

    out_time = models.DateTimeField(null=True, blank=True)
    in_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    gate_pass_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )
    def save(self, *args, **kwargs):
        # Generate gate pass ID only when approved
        if self.status == 'approved' and not self.gate_pass_id:
            self.gate_pass_id = f"GP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} | Room {self.room_no} | {self.status}"



    approved_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)








# models.py
from django.contrib.auth.models import User
from django.db import models

class WardenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


