from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class StudentRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Create username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Create password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }),
        }

    # -------------------------
    # Extra Profile Fields
    # -------------------------

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your full name"
        })
    )

    gender = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Male / Female"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
          "class": "form-control",
          "placeholder": "Enter email address"
        })
    )



    mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "10-digit mobile number"
        })
    )

    prn = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "PRN / Roll number"
        })
    )

    # ---- New Fields ----

    EDUCATION_LEVEL_CHOICES = [
        ('School', 'School'),
        ('Polytechnic', 'Polytechnic'),
        ('Engineering', 'Engineering'),
        ('BPharmacy', 'BPharmacy'),
        ('DPharmacy', 'DPharmacy'),
    ]

    education_level = forms.ChoiceField(
        choices=EDUCATION_LEVEL_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "education-level"
        })
    )

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

    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "year-select"
        })
    )

    sem = forms.ChoiceField(
        choices=SEM_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "sem-select"
        })
    )

    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Department (CSE / Mechanical...)"
        })
    )

    hostel = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Hostel name"
        })
    )

    room_no = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Room Number (Optional)"
        })
    )

    parent_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Parent / Guardian name"
        })
    )

    parent_mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Parent mobile number"
        })
    )



    parent_email = forms.EmailField(
    widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Parent email address"
    })
)






    
 



    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Full address"
        })
    )

    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "City"
        })
    )

    district = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "District"
        })
    )

    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "6-digit pincode"
        })
    )



#Student Login Form

class StudentLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password"
        })
    )




from django import forms
from .models import Gatepass
from django.utils import timezone


class GatepassForm(forms.ModelForm):

    class Meta:
        model = Gatepass
        fields = ['room_no', 'reason','destination']

from django import forms

class WardenLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
