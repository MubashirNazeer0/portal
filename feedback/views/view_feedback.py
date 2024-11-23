from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Feedback

class ViewAllFeedback(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            if kwargs:
                feedback_entries = Feedback.objects.filter(category=kwargs['cat'])
                return render(request, template_name="view_feedback.html", context={'feedback': feedback_entries, 'title': 'View Feedback'})

            feedback_entries = Feedback.objects.all()
            return render(request, template_name="view_feedback.html", context={'feedback': feedback_entries, 'title': 'View Feedback'})

        return render(request, template_name="dash/stalker.html", context={'title': 'Alert'} )

class ClearFeedbackView(LoginRequiredMixin, View):
    def get(self,request):
        Feedback.objects.all().delete()
        feedback_entries = Feedback.objects.all()
        return render(request, template_name="view_feedback.html" , context={'title':'View Feedback','feedback' :feedback_entries })

    def post(self,request):
        delete = Feedback.objects.all()
        delete.delete()