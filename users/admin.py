from django.contrib import admin
from .models import Profile,Employer,Student,Alumni

# Register your models here.
admin.site.register(Profile)
admin.site.register(Employer)
admin.site.register(Student)
admin.site.register(Alumni)
