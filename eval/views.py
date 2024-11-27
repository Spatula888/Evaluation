from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Faculty, Student, UserProfile

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        password = request.POST.get('password')

        if not role or not password:
            messages.error(request, 'Please provide all required details.')
            return render(request, 'login.html')

        try:
            # Authenticate based on role
            if role == 'admin':
                user_profile = UserProfile.objects.filter(is_admin=True).first()
            elif role == 'student':
                user_profile = Student.objects.first()  # Adjust for student criteria
            elif role == 'faculty':
                user_profile = Faculty.objects.first()  # Adjust for faculty criteria
            else:
                user_profile = None

            if user_profile:
                user = user_profile.user  # Get the associated user instance
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    # Redirect based on role
                    if role == 'admin':
                        return redirect('home')
                    elif role == 'student':
                        return redirect('student_dashboard')
                    elif role == 'faculty':
                        return redirect('faculty_dashboard')
                else:
                    messages.error(request, 'Invalid credentials.')

            else:
                messages.error(request, 'No user found for the selected role.')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'login.html')

def evaluation_list(request):
    # This view seems to just render a faculty login page
    return render(request, 'faculty-login.html')


@csrf_protect
def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        name = request.POST.get('name')
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        try:
            # Check if the username already exists
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                return render(request, 'register.html')

            # Create a new user
            user = User.objects.create_user(username=name, password=password)

            if role == 'admin':
                if UserProfile.objects.filter(is_admin=True).count() < 3:
                    UserProfile.objects.create(user=user, is_admin=True)
                else:
                    messages.error(request, 'Maximum admin users reached.')
                    return render(request, 'register.html')
            elif role == 'student':
                Student.objects.create(user=user, name=name)
            elif role == 'faculty':
                Faculty.objects.create(user=user, name=name)
            else:
                messages.error(request, 'Invalid role selected.')
                return render(request, 'register.html')

            messages.success(request, f'{role.capitalize()} registered successfully.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'register.html')


@login_required
def home_view(request):
    return render(request, 'home.html')
@login_required
def student_dashboard_view(request):
    # You can retrieve specific information for the student here, if needed
    return render(request, 'student_dashboard.html') 