from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.shortcuts import render
from ..forms import FeedbackForm
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

class FeedbackView(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        initial = {'username':request.user.username}
        form = FeedbackForm(instance=request.user, initial=initial, size = 8, maxChars=400)
        return render(request,
                      template_name='insert_feedback.html',
                      context={'form': form, 'title': 'Feedback Form'})

    def post(self, request, *args, **kwargs):
        initial = {'username':request.user.username}
        form = FeedbackForm(request.POST, initial=initial,size=8,maxChars=400)
        if form.is_valid():
            form = form.save(commit = False)
            form.user = Profile.objects.get(user_id=request.user.id)
            form.save()
            messages.success(request, f'Feedback has been submitted successfully')
            return render(request, "success.html", context={'title': 'Feedback Success'})

        return render(request, 'insert_feedback.html', {'form': form, 'title': 'Feedback Form'})


