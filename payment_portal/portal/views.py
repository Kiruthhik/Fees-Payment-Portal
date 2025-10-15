from django.shortcuts import render

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'portal/login.html')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portal.models import Student

@login_required
def home_view(request):
    # Get the logged-in user's email from Microsoft Entra ID login
    email = request.user.email.lower().strip()

    # Fetch student details from DB
    student = Student.objects.filter(email=email).first()

    if not student:
        return render(request, 'portal/home.html', {
            'error': 'Student record not found in database.',
        })

    # --- Fee Configuration Logic ---
    base_fee = 150000 if student.residence_type == 'day_scholar' else 200000
    admission_extra = 0 if student.admission_type == 'counselling' else 50000
    nri_extra = 100000 if student.is_nri else 0
    print(student.residence_type, student.admission_type, student.is_nri)
    total_fee = base_fee + admission_extra + nri_extra

    # For demonstration, assume 50,000 already paid
    paid_amount = 50000
    pending_amount = total_fee - paid_amount

    context = {
        'student': student,
        'total_fee': total_fee,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
    }
    print(context)
    return render(request, 'portal/home.html', context)
