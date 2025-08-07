from django.shortcuts import render

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'portal/login.html')

def home_view(request):
    # Render the home page
    return render(request, 'portal/home.html')