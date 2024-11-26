from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Advertisement,Posters
from users.models import Profile
from events.models import Events
from users.forms import EmployerSearchForm, StudentAlumniSearchForm

# Create your views here.
def welcome(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'users/welcome.html', {'advertisements': advertisements})

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'dash/home.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dash/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False









# class SearchUserView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):

#         if request.GET.get('query') != '':
#             search = request.GET.get('query')
#             users = Profile.objects.filter(Q(user__username__icontains=search) | Q(job_role__icontains=search) | Q(
#                 work_location__icontains=search) | Q(company__icontains=search) \
#                                            | Q(dept__iexact=search) | Q(registration_number__iexact=search)).order_by(
#                 '-user_id__date_joined')
#             context = {
#                 'title': 'Search User',
#                 'users': users,
#                 'query': search
#             }
#             return render(request, 'dash/search_list.html', context)
#         else:
#             return render(request, 'dash/home.html', {'title': 'Dash-Home'})

from django.db.models import Q
from datetime import datetime


# class SearchUserView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         user_type = request.user.profile.role  # Assuming you have the role stored in Profile model
        
#         # Determine the appropriate form based on user type
#         if user_type == 'employer':
#             form = EmployerSearchForm(request.GET)
#         else:  # for 'student' or 'alumni'
#             form = StudentAlumniSearchForm(request.GET)
        
#         search_results = None

#         # Get the values from the GET request (can be empty strings or None)
#         query = request.GET.get('query', '')
#         event_subject = request.GET.get('event_subject', '')
#         event_date = request.GET.get('event_date', '')
#         venue = request.GET.get('venue', '')
#         cgpa = request.GET.get('cgpa', '')
#         dept = request.GET.get('dept', '')
#         current_job = request.GET.get('current_job', '')
#         current_company = request.GET.get('current_company', '')
#         roll_no = request.GET.get('roll_no', '')

#         # Apply search filters only if the corresponding value is provided
#         if user_type == 'employer':
#             search_results = Profile.objects.filter(
#                 Q(user__username__icontains=query) |
#                 Q(cgpa__icontains=cgpa) |
#                 Q(dept__icontains=dept) |
#                 Q(job_role__icontains=current_job) |
#                 Q(company__icontains=current_company) |
#                 Q(registration_number__icontains=roll_no)
#             ).order_by('-id')
#         else:  # For student or alumni
#             # Build the filter conditions
#             filters = Q()
            
#             # Apply filters only for non-empty fields
#             if event_subject:
#                 print('evemt subject present',event_subject)
#                 filters &= Q(event_subject__icontains=event_subject)
            
#             if event_date:
#                 try:
#                     # Validate the date format and apply the filter if valid
#                     datetime.strptime(event_date, '%Y-%m-%d')
#                     filters &= Q(event_date__exact=event_date)
#                 except ValueError:
#                     pass  # If invalid date format, ignore the filter
            
#             if venue:
#                 filters &= Q(venue__icontains=venue)
#             search_results = Events.objects.filter(filters)
#         context = {
#             'title': 'Search Results',
#             'form': form,
#             'query': query,
#             'search_results': search_results
#         }
#         print(search_results)
#         return render(request, 'dash/search_list.html', context)
class SearchUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_type = request.user.profile.role  # Assuming you have the role stored in Profile model
        
        # Determine the appropriate form based on user type
        if user_type == 'employer':
            form = EmployerSearchForm(request.GET)
        else:  # for 'student' or 'alumni'
            form = StudentAlumniSearchForm(request.GET)
        
        search_results = None

        # Get the values from the GET request (can be empty strings or None)
        query = request.GET.get('query', '')
        dept = request.GET.get('dept', '')
        cgpa = request.GET.get('cgpa', '')
        passout_year = request.GET.get('passout_year', '')
        current_job = request.GET.get('current_job', '')
        current_company = request.GET.get('current_company', '')
        roll_no = request.GET.get('roll_no', '')

        if user_type == 'employer':
            # Employers search Students and Alumni
            student_filters = Q()
            alumni_filters = Q()

            # Apply filters for students
            if dept:
                student_filters &= Q(dept__icontains=dept)
            if cgpa:
                student_filters &= Q(cgpa__gte=float(cgpa))  # e.g., cgpa >= entered value
            if passout_year:
                student_filters &= Q(passout_year=passout_year)
            if roll_no:
                student_filters &= Q(registration_number__icontains=roll_no)

            # Apply filters for alumni
            if dept:
                alumni_filters &= Q(dept__icontains=dept)
            if cgpa:
                alumni_filters &= Q(cgpa__gte=float(cgpa))  # e.g., cgpa >= entered value
            if passout_year:
                alumni_filters &= Q(passout_year=passout_year)
            if current_job:
                alumni_filters &= Q(current_job__icontains=current_job)
            if current_company:
                alumni_filters &= Q(current_company__icontains=current_company)

            # Combine results from both models
            student_results = Student.objects.filter(student_filters)
            alumni_results = Alumni.objects.filter(alumni_filters)
            
            # Combine QuerySets
            search_results = list(student_results) + list(alumni_results)
        else:
            # Students or alumni searching events
            filters = Q()
            event_subject = request.GET.get('event_subject', '')
            event_date = request.GET.get('event_date', '')
            venue = request.GET.get('venue', '')

            if event_subject:
                filters &= Q(event_subject__icontains=event_subject)
            if event_date:
                try:
                    datetime.strptime(event_date, '%Y-%m-%d')
                    filters &= Q(event_date=event_date)
                except ValueError:
                    pass  # Ignore invalid dates
            if venue:
                filters &= Q(venue__icontains=venue)
            
            search_results = Events.objects.filter(filters)

        context = {
            'title': 'Search Results',
            'form': form,
            'query': query,
            'search_results': search_results,
        }
        return render(request, 'dash/search_list.html', context)





def about(request):
    return render(request, 'dash/about.html', {'title': 'About'})




from django.shortcuts import render, redirect ,get_object_or_404
from users.models import Profile
from users.forms import AdvertisementForm,PostersForm
from .models import Advertisement


def manage_pending_profiles(request):
    pending_profiles = Profile.objects.filter(status='pending')
    print(f"Pending Profiles Count: {len(pending_profiles)}")  # Print count of pending profiles
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        profile = Profile.objects.get(id=user_id)
        
        if action == 'approve':
            profile.status = 'approved'
        elif action == 'disapprove':
            profile.status = 'disapproved'
        
        profile.save()
        return redirect('manage_pending_profiles')

    return render(request, 'dash/manage_pending_profiles.html', {
        'pending_profiles': pending_profiles,
    })



def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)  # Handle image upload
        if form.is_valid():
            form.save()
            return redirect('advertisement_list')  # Redirect to the advertisement listing page after adding
    else:
        form = AdvertisementForm()

    return render(request, 'dash/add_advertisement.html', {'form': form})

def advertisement_list(request):
    advertisements = Advertisement.objects.all()  # Get all advertisements from the database
    print(advertisements)  # Print to check if any data exists
    return render(request, 'dash/advertisement_list.html', {'advertisements': advertisements})

def delete_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        advertisement.delete()
        return redirect('advertisement_list')  # Redirect after successful deletion
    return render(request, 'dash/delete_advertisement.html', {'advertisement': advertisement})

def add_posters(request):
    if request.method == 'POST':
        form = PostersForm(request.POST, request.FILES)  # Handle image upload
        if form.is_valid():
            form.save()
            return redirect('posters_list')  # Redirect to the advertisement listing page after adding
    else:
        form = PostersForm()

    return render(request, 'dash/add_posters.html', {'form': form})

def posters_list(request):
    advertisements = Posters.objects.all()  # Get all advertisements from the database
    print(advertisements)  # Print to check if any data exists
    return render(request, 'dash/posters_list.html', {'advertisements': advertisements})