from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, ProfileRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.views import LoginView


# Create your views here.

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         profile_form = ProfileRegisterForm(request.POST)
#         if form.is_valid() and profile_form.is_valid():
#             try:
#                 user = form.save()
#                 userprofile = Profile.objects.get(user=user)
#                 userprofile.dept=profile_form.cleaned_data['dept']
#                 userprofile.registration_number=profile_form.cleaned_data['registration_number'].upper()
#                 userprofile.job_role=profile_form.cleaned_data['job_role']
#                 userprofile.work_location=profile_form.cleaned_data['work_location']
#                 userprofile.company=profile_form.cleaned_data['company']
#                 userprofile.passout_year = profile_form.cleaned_data['passout_year']
#                 userprofile.save()
#                 username = form.cleaned_data.get('username')
#                 raw_password = form.cleaned_data.get('password1')
#                 messages.success(request, f'Your account has been created successfully')
#                 user = authenticate(username=username, password=raw_password)
#                 # login(request, user)
#                 # return redirect('dash-home')
#                 messages.warning(request, f'You Can Login Once the Admin approves your account')
#                 return redirect('login')
            
#             except Exception as e:
#                 print(e)
#                 messages.warning(request, f'There was some issue')
#                 return redirect('login')
#     else:
#         form = UserRegisterForm()
#         profile_form = ProfileRegisterForm()
#     return render(request, 'users/register.html', {'form': form, 'profile_form': profile_form})





from .forms import UserRegisterForm, ProfileRegisterForm, EmployerForm, StudentForm,AlumniForm

# def register(request):
#     if request.method == 'POST':
#         # Load the user registration and profile forms
#         form = UserRegisterForm(request.POST)
#         profile_form = ProfileRegisterForm(request.POST)

#         if form.is_valid() and profile_form.is_valid():
#             try:
#                 # Save the user instance
#                 user = form.save()
#                 role = profile_form.cleaned_data['role']

#                 # Create the profile instance
#                 profile = Profile.objects.create(user=user, role=role)

#                 # Handle specific role-based forms
#                 if role == 'employer':
#                     employer_form = EmployerForm(request.POST)
#                     if employer_form.is_valid():
#                         employer = employer_form.save(commit=False)
#                         employer.profile = profile
#                         employer.save()
#                     else:
#                         messages.error(request, "Error in Employer Form.")
#                         raise ValueError("Invalid Employer Form")

#                 elif role == 'student':
#                     student_form = StudentForm(request.POST)
#                     if student_form.is_valid():
#                         student = student_form.save(commit=False)
#                         student.profile = profile
#                         student.save()
#                     else:
#                         messages.error(request, "Error in Student Form.")
#                         raise ValueError("Invalid Student Form")

#                 # Success messages and redirect
#                 messages.success(request, 'Your account has been created successfully.')
#                 messages.warning(request, 'You can log in once the admin approves your account.')
#                 return redirect('login')

#             except Exception as e:
#                 print(f"Error: {e}")
#                 messages.error(request, 'There was an issue creating your account. Please try again.')

#         else:
#             messages.error(request, 'Please correct the errors in the form.')

#     else:
#         # Render empty forms for GET request
#         form = UserRegisterForm()
#         profile_form = ProfileRegisterForm()
#         employer_form = EmployerForm()
#         student_form = StudentForm()

#     return render(request, 'users/register.html', {
#         'form': form,
#         'profile_form': profile_form,
#         'employer_form': employer_form,
#         'student_form': student_form,
#     })
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            # Check if the user already has a profile
            profile, created = Profile.objects.get_or_create(user=user)  # This will get the existing profile or create a new one
            
            if created:  # Profile was newly created
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()  # Save the new profile
            else:  # Profile already exists, maybe update it
                # Optionally update fields if needed, e.g., update role, dept, etc.
                profile_form.save(commit=False)  # If needed, update fields here
                profile.save()

            # Proceed with saving the specific model (Employer, Student, Alumni)
            role = profile_form.cleaned_data['role']
            if role == 'employer':
                employer_form = EmployerForm(request.POST)
                if employer_form.is_valid():
                    employer = employer_form.save(commit=False)
                    employer.profile = profile
                    employer.save()
            elif role == 'student':
                student_form = StudentForm(request.POST, prefix='student')
                if student_form.is_valid():
                    student = student_form.save(commit=False)
                    student.profile = profile
                    student.save()
            elif role == 'alumni':
                alumni_form = AlumniForm(request.POST, prefix='alumni')
                if alumni_form.is_valid():
                    alumni = alumni_form.save(commit=False)
                    alumni.profile = profile
                    alumni.save()

            # login(request, user)
            return redirect('login')
    else:
        # Render empty forms for GET request
        form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        employer_form = EmployerForm()
        student_form = StudentForm()
        alumni_form=AlumniForm()
    return render(request, 'users/register.html', {
        'form': form,
        'profile_form': profile_form,
        'employer_form': employer_form,
        'student_form': student_form,
        'alumni_form':alumni_form
    })






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


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Redirect authenticated users to home

    def form_valid(self, form):
        # Call the parent form_valid method to authenticate the user
        user = form.get_user()
        profile = Profile.objects.get(user=user)
        
        # Check if the user's profile is approved
        if profile.status == 'approved':
            # If approved, log the user in and redirect to home
            login(self.request, user)
            return redirect('dash-home')  # Or the page where you want the user to go
        else:
            # If not approved, show an error message and redirect to login page
            messages.error(self.request, 'Your account is not approved yet. Please contact the admin.')
            return redirect('login')  # Stay on the login page
        
        
        
def custom_logout(request):
    auth_views.LogoutView.as_view()(request)
    return redirect('welcome')  # Replace 'welcome' with the name of your welcome page's URL
