from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.views import LoginView
from django.db import transaction

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegisterForm(request.POST)
#         profile_form = ProfileRegisterForm(request.POST, request.FILES)  # Include request.FILES
#         student_form = StudentForm(request.POST, request.FILES, prefix='student')  # Include request.FILES

#         if user_form.is_valid() and profile_form.is_valid() and student_form.is_valid():
#             try:
#                 # Start a transaction block
#                 with transaction.atomic():
#                     # Save the user
#                     user = user_form.save()

#                     # Check if the user already has a profile
#                     profile, created = Profile.objects.get_or_create(user=user)

#                     if created:  # Profile was newly created
#                         profile = profile_form.save(commit=False)
#                         profile.user = user
#                         profile.role = profile_form.cleaned_data['role']  # Set role from the form
#                         profile.save()  # Save the new profile
#                     else:  # Profile already exists, maybe update it
#                         profile.role = profile_form.cleaned_data['role']  # Update role field
#                         profile.save()  # Save the updated profile

#                     # Proceed with saving the specific model (Employer, Student, Alumni)
#                     role = profile_form.cleaned_data['role']
#                     if role == 'employer':
#                         employer_form = EmployerForm(request.POST, request.FILES)  # Include request.FILES
#                         if employer_form.is_valid():
#                             employer = employer_form.save(commit=False)
#                             employer.profile = profile
#                             employer.save()
#                         else:
#                             raise ValueError("Employer form is invalid.")
#                     elif role == 'student':
#                         student = student_form.save(commit=False)
#                         student.profile = profile
#                         student.save()
#                         # Handle CV file upload
#                         cv = student_form.cleaned_data.get('cv')  # Get the uploaded CV
#                         if cv:
#                             student.cv = cv  # Save the CV to the student instance
#                             student.save()

#                     elif role == 'alumni':
#                         alumni_form = AlumniForm(request.POST, prefix='alumni')
#                         if alumni_form.is_valid():
#                             alumni = alumni_form.save(commit=False)
#                             alumni.profile = profile
#                             alumni.save()
                            
                            
#                             cv = alumni_form.cleaned_data.get('cv')  # Get the uploaded CV
#                             if cv:
#                                 alumni.cv = cv  # Save the CV to the student instance
#                                 alumni.save()

#                         else:
#                             raise ValueError("Alumni form is invalid.")

#                     # Transaction successful, redirect to login
#                     return redirect('login')

#             except Exception as e:
#                 # Log the error for debugging (optional)
#                 print(f"An error occurred: {e}")

#                 # Optionally, add a message to the user
#                 messages.error(request, "An error occurred during registration. Please try again.")
#         else:
#             messages.error(request, "Invalid form data. Please correct the errors below.")

#     else:
#         # Render empty forms for GET request
#         user_form = UserRegisterForm()
#         profile_form = ProfileRegisterForm()
#         employer_form = EmployerForm()
#         student_form = StudentForm(prefix='student')
#         alumni_form = AlumniForm(prefix='alumni')

#     return render(request, 'users/register.html', {
#         'form': user_form,
#         'profile_form': profile_form,
#         'employer_form': employer_form,
#         'student_form': student_form,
#         'alumni_form': alumni_form
#     })

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        student_form = StudentForm(request.POST, request.FILES, prefix='student')

        if user_form.is_valid() and profile_form.is_valid() and student_form.is_valid():
            try:
                with transaction.atomic():
                    # Save the user
                    user = user_form.save()

                    # Check if the user already has a profile
                    profile, created = Profile.objects.get_or_create(user=user)

                    if created:
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.role = profile_form.cleaned_data['role']
                        profile.save()
                    else:
                        profile.role = profile_form.cleaned_data['role']
                        profile.save()

                    # Handle roles
                    role = profile_form.cleaned_data['role']
                    if role == 'employer':
                        employer_form = EmployerForm(request.POST, request.FILES)
                        if employer_form.is_valid():
                            employer = employer_form.save(commit=False)
                            employer.profile = profile
                            employer.save()
                        else:
                            raise ValueError("Employer form is invalid.")
                    elif role == 'student':
                        # Manually set the CV field and save
                        student = student_form.save(commit=False)
                        student.profile = profile
                        print(request.FILES)
                        print(student_form.cleaned_data.get('cv'))
                        # Retrieve and assign CV from form data
                        cv = request.FILES.get(student_form.add_prefix('cv'))  # Retrieve 'cv' from FILES
                        if cv:
                            student.cv = cv

                        student.save()
                    elif role == 'alumni':
                        alumni_form = AlumniForm(request.POST, request.FILES, prefix='alumni')
                        if alumni_form.is_valid():
                            alumni = alumni_form.save(commit=False)
                            alumni.profile = profile

                            # Retrieve and assign CV from form data
                            cv = request.FILES.get(alumni_form.add_prefix('cv'))
                            if cv:
                                alumni.cv = cv

                            alumni.save()
                        else:
                            raise ValueError("Alumni form is invalid.")

                    # Redirect on success
                    return redirect('login')

            except Exception as e:
                print(f"An error occurred: {e}")
                messages.error(request, "An error occurred during registration. Please try again.")
        else:
            messages.error(request, "Invalid form data. Please correct the errors below.")

    else:
        # Render forms for GET request
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        employer_form = EmployerForm()
        student_form = StudentForm(prefix='student')
        alumni_form = AlumniForm(prefix='alumni')

    return render(request, 'users/register.html', {
        'form': user_form,
        'profile_form': profile_form,
        'employer_form': employer_form,
        'student_form': student_form,
        'alumni_form': alumni_form
    })













































# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegisterForm(request.POST)
#         profile_form = ProfileRegisterForm(request.POST, request.FILES)  # Include request.FILES
#         student_form = StudentForm(request.POST, request.FILES, prefix='student')  # Include request.FILES
#         employer_form = EmployerForm(request.POST, request.FILES)  # Include request.FILES
#         alumni_form = AlumniForm(request.POST, request.FILES, prefix='alumni')  # Include request.FILES

#         if user_form.is_valid() and profile_form.is_valid() and student_form.is_valid():
#             try:
#                 with transaction.atomic():
#                     # Save user and profile
#                     user = user_form.save()
#                     profile = profile_form.save(commit=False)
#                     profile.user = user
#                     profile.save()

#                     # Save role-specific data
#                     role = profile_form.cleaned_data['role']
#                     if role == 'employer' and employer_form.is_valid():
#                         employer = employer_form.save(commit=False)
#                         employer.profile = profile
#                         employer.save()
#                     elif role == 'student' and student_form.is_valid():
#                         student = student_form.save(commit=False)
#                         student.profile = profile
#                         student.save()
#                     elif role == 'alumni' and alumni_form.is_valid():
#                         alumni = alumni_form.save(commit=False)
#                         alumni.profile = profile
#                         alumni.save()
#                     else:
#                         raise ValueError("Invalid role-specific form data.")

#                     # Redirect on success
#                     return redirect('login')

#             except Exception as e:
#                 messages.error(request, f"An error occurred: {e}")
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         # Initialize forms for GET request
#         user_form = UserRegisterForm()
#         profile_form = ProfileRegisterForm()
#         employer_form = EmployerForm()  # Initialize EmployerForm
#         student_form = StudentForm(prefix='student')  # Initialize StudentForm
#         alumni_form = AlumniForm(prefix='alumni')  # Initialize AlumniForm

#     return render(request, 'users/register.html', {
#         'form': user_form,
#         'profile_form': profile_form,
#         'employer_form': employer_form,
#         'student_form': student_form,
#         'alumni_form': alumni_form
#     })



















@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def view_profile(request, *args, **kwargs):
    """
    should pass the id of the user object as an argument to this function for this to work
    """

    if request.method == 'GET':
        profile_user = Profile.objects.get(user_id=kwargs['id'])
        # user = User.objects.get(id = kwargs['id'])
        # profile_user = Profile.objects.get(user_id = user.id)
        return render(request, 'users/view_profile.html', context={'view_user': profile_user, 'title': 'User Profile'})

    return render(request, 'users/view_profile.html', context={'title': 'User Profile'})


@login_required
def update_password(request, *args, **kwargs):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f'Password updated successfully')
            return HttpResponseRedirect('logout')
        else:
            messages.warning(request, f"Passwords doesn't pass the required criteria or doesn't match.Please check")
            return render(request, template_name='users/profile.html')
    else:
        password_form = PasswordChangeForm(request.user)
        context = {
            'password_form': password_form,
            'title': 'Change Password'
        }
    return render(request, 'users/profile.html', context=context)


# class CustomLoginView(LoginView):
#     template_name = 'users/login.html'
#     redirect_authenticated_user = True  # Redirect authenticated users to home

#     def form_valid(self, form):
#         # Call the parent form_valid method to authenticate the user
#         user = form.get_user()
#         profile = Profile.objects.get(user=user)
        
#         # Check if the user's profile is approved
#         if profile.status == 'approved':
#             # If approved, log the user in and redirect to home
#             login(self.request, user)
#             return redirect('dash-home')  # Or the page where you want the user to go
#         else:
#             # If not approved, show an error message and redirect to login page
#             messages.error(self.request, 'Your account is not approved yet. Please contact the admin.')
#             return redirect('login')  # Stay on the login page
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm  # Use the custom form

    def form_valid(self, form):
        user = form.get_user()
        profile = Profile.objects.get(user=user)
        selected_role = form.cleaned_data.get('role')

        if profile.status == 'approved':
            if profile.role == selected_role:
                login(self.request, user)
                return redirect('dash-home')  # Redirect to the appropriate page
            else:
                messages.error(self.request, f"Incorrect role selected for user {user.username}.")
                return redirect('login')
        else:
            messages.error(self.request, 'Your account is not approved yet. Please contact the admin.')
            return redirect('login')
       
        
        
def custom_logout(request):
    auth_views.LogoutView.as_view()(request)
    return redirect('welcome')  # Replace 'welcome' with the name of your welcome page's URL
