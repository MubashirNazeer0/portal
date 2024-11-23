from django.db import models
from users.models import Profile

# Create your models here.
INFRASTRCUTURE = 'INF'
GENERIC = 'GEN'
CURRICULUM = 'CUR'


class Feedback(models.Model):

    FEEDBACK_CHOICES = (
        (INFRASTRCUTURE,'Infrastructure'),
        (GENERIC,'Generic'),
        (CURRICULUM,'Curriculum'),
    )


    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.CharField(max_length=3,
                                choices = FEEDBACK_CHOICES,
                                default=GENERIC)
    date_added = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=400)
    email= models.EmailField()

    def __str__(self):
        return self.user.user_id