from django.contrib.postgres.fields import ArrayField, IntegerRangeField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year() + 1)(value)


# Create your models here.
MM = 'Management and Marketing'
MIS = 'Management and Information System'
FFI = 'Finance and Financial Institutions'
GA = 'General Administration'
AC = 'Accounting'
OM = 'Operations Management'
ECON='Economics'
NONE = ''


class Profile(models.Model):
    """
    User objects have the following fields
    username
    first_name
    last_name
    email
    password
    event_id
    """
    DEPT_CHOICES = (
        ('NONE', ''),
        ('MM', 'MANAGEMENT AND MARKETING'),
        ('MIS', 'MANAGEMENT AND INFORMATION SYSTEM'),
        ('FFI', 'FINANCE AND FINANCIAL INSTITUTIONS'),
        ('GA', 'GENERAL ADMINISTRATION'),
        ('AC', 'ACCOUNTING'),
        ('OM', 'OPERATIONS MANAGEMENT'),
        ('ECON','ECONOMICS')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    dept = models.CharField(max_length=120,
                            choices=DEPT_CHOICES,
                            default=NONE,
                            null=True)
    registration_number = models.CharField(max_length=12, blank=True, null=True)
    job_role = models.CharField(max_length=100,blank=True,null=True)
    work_location = models.CharField(max_length=100,blank=True,null=True)
    company = models.CharField(max_length=200,blank=True,null=True)
    passout_year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    event_ids = models.TextField(default=None, null=True, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return f'{self.user.username} Profile'

    # Resizing the image to a smaller size
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @staticmethod
    def year_choices():
        return [(r, r) for r in range(1984, datetime.date.today().year + 2)]


class Employer(models.Model):
    """
    Model specific to Employers.
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    work_location = models.CharField(max_length=200)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    Description=models.TextField(max_length=800,blank=True,null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f'{self.profile.user.username} - Employer'


class Student(models.Model):
    """
    Model specific to Students.
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    dept = models.CharField(max_length=120, choices=Profile.DEPT_CHOICES, default='NONE', null=True)
    id_number = models.CharField(max_length=12, blank=True, null=True)
    cgpa = models.FloatField(null=False,blank=True,default=0.0)
    passout_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
    )
    AdmissionYear = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
    )    
    cv = models.FileField(upload_to='student_cvs/', null=True, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f'{self.profile.user.username} - Student'
    
    
    
# Alumni model, linked to the Profile model
class Alumni(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
    DEPT_CHOICES = (
        ('NONE', ''),
        ('MM', 'MANAGEMENT AND MARKETING'),
        ('MIS', 'MANAGEMENT AND INFORMATION SYSTEM'),
        ('FFI', 'FINANCE AND FINANCIAL INSTITUTIONS'),
        ('GA', 'GENERAL ADMINISTRATION'),
        ('AC', 'ACCOUNTING'),
        ('OM', 'OPERATIONS MANAGEMENT'),
    )
    dept = models.CharField(max_length=120, choices=Profile.DEPT_CHOICES, default='NONE', null=True)
    id_number = models.CharField(max_length=12, blank=True, null=True)
    cgpa = models.FloatField(null=False,blank=True,default=0.0)
    passout_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
    )
    current_job = models.CharField(max_length=200, blank=True, null=True)
    current_company = models.CharField(max_length=200, blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    cv = models.FileField(upload_to='alumni_cvs/', null=True, blank=True)
    status = models.CharField(max_length=12, choices=Profile.STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.profile.user.username} - Alumni'