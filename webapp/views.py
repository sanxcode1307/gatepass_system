from django.shortcuts import render,redirect

# Create your views here.

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import StudentRegisterForm,StudentLoginForm
from .models import StudentProfile



# -----------------------------
#   REGISTER VIEW
# -----------------------------
def register_page(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)

        if form.is_valid():
            # Save User
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            # Save Student Profile
            StudentProfile.objects.create(
                user=user,
                full_name=form.cleaned_data["full_name"],
                gender=form.cleaned_data["gender"],
                mobile=form.cleaned_data["mobile"],
                prn=form.cleaned_data["prn"],
                education_level=form.cleaned_data["education_level"],
                year=form.cleaned_data["year"],
                sem=form.cleaned_data["sem"],
                department=form.cleaned_data["department"],
                hostel=form.cleaned_data["hostel"],
                room_no=form.cleaned_data["room_no"],
                parent_name=form.cleaned_data["parent_name"],
                parent_mobile=form.cleaned_data["parent_mobile"],
                parent_email=form.cleaned_data['parent_email'],  # 👈 IMPORTANT
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                district=form.cleaned_data["district"],
                pincode=form.cleaned_data["pincode"],
            )

            
            messages.success(request, "Registration successful!")
            messages.success(request, "Registration successful! Please login now.")
            return redirect("login") 
            return redirect("login") 
        else:
      
            return render(request, "register.html", {"form": form})

    else:
   
        form = StudentRegisterForm()
        return render(request, "register.html", {"form": form})



def login_page(request):
    if request.method == "POST":
        form = StudentLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("student_dashboard")   # update with your homepage name

    else:
        form = StudentLoginForm()

    return render(request, "login.html", {"form": form})
    

@login_required
def student_dashboard(request):
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, "student_dashboard.html", {"profile": profile})



#Apply Gatepass View
from django.shortcuts import render, redirect
from .forms import GatepassForm
from .models import Gatepass

def apply_gatepass(request):
    if request.method == 'POST':
        form = GatepassForm(request.POST)
        if form.is_valid():
            gatepass = form.save(commit=False)
            gatepass.student = request.user
            gatepass.save()
            return redirect('success')
    else:
        form = GatepassForm()

    return render(request, 'apply_gatepass.html', {'form': form})

def success(request):
    return render(request, 'success.html')





def warden_dashboard(request):
    gatepasses = Gatepass.objects.select_related(
        'student',
        'student__studentprofile'
    ).order_by('-created_at')

    return render(request, 'warden_dashboard.html', {
        'gatepasses': gatepasses
    })


from django.shortcuts import get_object_or_404, redirect
from .models import Gatepass
from django.core.mail import send_mail
from django.conf import settings
import uuid
@login_required

def approve_gatepass(request, pk):
    gatepass = get_object_or_404(Gatepass, pk=pk)

    gatepass.status = 'approved'
    if not gatepass.gate_pass_id:
        gatepass.gate_pass_id = f"GP-{uuid.uuid4().hex[:8].upper()}"
    gatepass.save()

    student_email = gatepass.student.email  # ✅ yahi se email

    send_mail(
        subject="Gatepass Approved",
        message=(
            f"Hello {gatepass.student.username},\n\n"
            f"Your gatepass has been approved.\n"
            f"Gatepass ID: {gatepass.gate_pass_id}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student_email],
        fail_silently=False,
    )

    if gatepass.approved_at is None:  # important
        gatepass.approved_at = timezone.now()

    gatepass.save()

    return redirect('warden_dashboard')


@login_required
def reject_gatepass(request, pk):
    gp = Gatepass.objects.get(id=pk)
    gp.status = 'rejected'
    gp.save()
    
    return redirect('warden_dashboard')


def close_gatepass(request, id):
    gatepass = GatePass.objects.get(id=id)
    gatepass.status = "Closed"

    if gatepass.closed_at is None:
        gatepass.closed_at = timezone.now()

    gatepass.save()
  



from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Gatepass

# 1️⃣ Warden Dashboard
def warden_dashboard(request):
    gatepasses = Gatepass.objects.all().order_by('-created_at')
    context = {
        'gatepasses': gatepasses
    }
    return render(request, 'warden_dashboard.html', context)



# 3️⃣ Reject Gatepass
def reject_gatepass(request, pk):
    gp = get_object_or_404(Gatepass, pk=pk)
    if gp.status == "pending":
        gp.status = "rejected"
        gp.save()

        # Optional: send email to parent about rejection
        subject = f"{gp.student.studentprofile.full_name}'s Gatepass Rejected"
        message = f"""
Hello {gp.student.studentprofile.parent_name},

Your child {gp.student.studentprofile.full_name}'s gatepass request has been rejected.

Gatepass Details:
- Reason: {gp.reason}
- Applied On: {gp.created_at.strftime('%d-%b-%Y %I:%M %p')}

Regards,
Hostel Management System
"""
        parent_email = gp.student.studentprofile.parent_email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [parent_email], fail_silently=True)

    return redirect('warden_dashboard')


# 4️⃣ Close Gatepass (Student Returned)
def close_gatepass(request, pk):
    gp = get_object_or_404(Gatepass, pk=pk)
    if gp.status == "approved":
        gp.status = "returned"
        gp.returned_at = timezone.now()
        gp.save()

        # Send email to parent
        subject = f"{gp.student.studentprofile.full_name} has returned from home"
        message = f"""
Hello {gp.student.studentprofile.parent_name},

Your child {gp.student.studentprofile.full_name} has returned safely from home.

Gatepass Details:
- Approved On: {gp.approved_at.strftime('%d-%b-%Y %I:%M %p')}
- Returned On: {gp.returned_at.strftime('%d-%b-%Y %I:%M %p')}

Regards,
Hostel Management System
"""
        parent_email = gp.student.studentprofile.parent_email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [parent_email], fail_silently=False)

    return redirect('warden_dashboard')

from webapp.models import Gatepass

def warden_dashboard(request):
    gatepasses = Gatepass.objects.all().order_by('-created_at')  # latest first
    return render(request, 'warden_dashboard.html', {'gatepasses': gatepasses})





# webapp/views.py
from django.shortcuts import render

def home(request):
    """
    HMS Home Page
    """
    return render(request, 'home.html')



# views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

def warden_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:   # Warden check
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('warden_dashboard')
            else:
                messages.error(request, "You are not authorized as warden")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'warden_login.html')


