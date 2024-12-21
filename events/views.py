from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import EventsCreation
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
import requests
from datetime import datetime
from libs.mailgun import Mailgun
import json
from django.core.mail import EmailMultiAlternatives
from .models import Events, Poll

# class events_creation(LoginRequiredMixin,View):
#     def get(self, request, *args, **kwargs):
#         initial = {'username': request.user.username}
#         form = EventsCreation(instance=request.user, initial=initial)

#         #for updating the event
#         if kwargs:
#             event = get_object_or_404(Events,id=kwargs['id'])
#             form = EventsCreation(instance = event,initial = initial)
#             return render(request,template_name='create_event.html',context={'event_id':event.id,'form':form,'title':'Event Form','user_logged':request.user})

#         return render(request,template_name='create_event.html',context={'form': form, 'title': 'Event Form','user_logged':request.user})


#     def post(self, request, *args, **kwargs):
#         initial = {'username': request.user.username}
#         form = EventsCreation(request.POST, initial=initial)
#         if form.is_valid():
#             #update_or_create should be done
#             form = form.save(commit = False)
#             form.user = get_object_or_404(User,id=request.user.id)
#             if request.POST.get('event_id'):
#                 event = Events.objects.get(pk = int(request.POST.get('event_id').strip('/')))
#                 form = EventsCreation(data=request.POST,instance=event)
#                 form.save()
#                 messages.success(request, f'Event has been updated successfully')
#             else:
#                 form.save()
#                 messages.success(request, send_creation_message(form.id))
#                 messages.success(request, f'Event created successfully')
#             return render(request,"succes.html", context={'title': 'Event Success'})

#         return render(request, 'create_event.html', {'form': form, 'title': 'Event Form','user_logged':request.user})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import EventsCreation
from django.contrib import messages

class events_creation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        initial = {'username': request.user.username}
        form = EventsCreation(instance=request.user, initial=initial)

        # For updating the event
        if kwargs:
            event = get_object_or_404(Events, id=kwargs['id'])
            form = EventsCreation(instance=event, initial=initial)
            return render(request, template_name='create_event.html', context={'event_id': event.id, 'form': form, 'title': 'Event Form', 'user_logged': request.user})

        return render(request, template_name='create_event.html', context={'form': form, 'title': 'Event Form', 'user_logged': request.user})

    def post(self, request, *args, **kwargs):
        initial = {'username': request.user.username}
        form = EventsCreation(request.POST, request.FILES, initial=initial)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form = form.save(commit=False)
            form.user = get_object_or_404(User, id=request.user.id)
            
            if request.POST.get('event_id'):
                event = Events.objects.get(pk=int(request.POST.get('event_id').strip('/')))
                form = EventsCreation(data=request.POST, instance=event)
                form.save()
                messages.success(request, f'Event has been updated successfully')
            else:
                form.save()
                messages.success(request, f'Event created successfully')
                
            return render(request, "succes.html", context={'title': 'Event Success'})

        return render(request, 'create_event.html', {'form': form, 'title': 'Event Form', 'user_logged': request.user})

class view_events(View):
    def get(self, request):
        # poll = Poll.objects.all()
        #taking current user id
        auth_id = request.user.id
        user_id = None
        if auth_id != None:
            user_id = Profile.objects.get(user_id=auth_id)
            user_id = user_id.id
        #if the user is logged in we show polls for user to vote
        if user_id != None:
            user = Profile.objects.get(id=user_id)
            jsonDec = json.decoder.JSONDecoder()
            query_results = Events.objects.all().order_by('-date_added')

            #if the user has never voted in the poll before then we send false ids to the template
            #else we send the event ids which user has voted before as true for the template to show the vote persentages
            # if user.event_ids is None:
            #     ids = [False]*len(query_results)
            # else:
            #     ids = [True if x.id in jsonDec.decode(user.event_ids) else False for x in query_results]

            # query_results = zip(query_results,ids)
            context={'query_results':query_results,'user_logged':request.user,'profile_id':user_id}
            return render(request, template_name="view_events.html",context=context)
        #this is the part where we won't send the poll info to the template to display
        else:
            query_results = Events.objects.all()
            # ids = [False] * len(query_results)
            # query_results = zip(query_results)
            context = {'query_results': query_results,'profile_id':None, 'user_logged': None}
            return render(request, template_name="view_events.html", context=context)


    def post(self, request):
        event_id = int(request.POST.get('event_id'))
        auth_id = request.user.id
        user = Profile.objects.get(user_id=auth_id)
        user_id = user.id
        try:
            #check if the record has been already there for the poll with this current user or create one
            poll = Poll.objects.get_or_create(event_id=event_id)[0]

            #incrementing the yes count if poll result is 1 then increment yes count
            if(int(request.POST.get('result'))):
                poll.yes_count += 1
                send_registration_message(event_id, request.user)
            #and if it is 0 then increment no count
            else:
                poll.no_count += 1
            poll.save()
            #if user is voting for the first time then dump the event id in the user data as it is
            if user.event_ids is None:
                event_ids = []
                event_ids.append(int(request.POST.get('event_id')))
                user.event_ids = json.dumps(event_ids)
            #append the new event_id to the existing event_ids in the user data
            else:
                jsonDec = json.decoder.JSONDecoder()
                ids = jsonDec.decode(user.event_ids)
                ids.append(event_id)
                user.event_ids = json.dumps(ids)
            user.save()
        except Exception:
            event = Events.objects.get(id = event_id)
            yes_count = 0
            no_count = 0
            if (int(request.POST.get('result'))):
                yes_count = 1
                send_registration_message(event_id, request.user)
            else:
                no_count = 1
            poll = Poll(event_id=event,yes_count=yes_count,no_count=no_count)
            poll.save()
            if user.event_ids is None:
                event_ids = []
                event_ids.append(int(request.POST.get('event_id')))
                user.event_ids = json.dumps(event_ids)
            else:
                jsonDec = json.decoder.JSONDecoder()
                ids = jsonDec.decode(user.event_ids)
                ids.append(event_id)
                user.event_ids = json.dumps(ids)
            user.save()
        query_results = Events.objects.all()
        jsonDec = json.decoder.JSONDecoder()
        ids = [True if x.id in jsonDec.decode(user.event_ids) else False for x in query_results]
        query_results = zip(query_results, ids)
        poll = Poll.objects.all()
        context = {'query_results': query_results,'user_logged': request.user,'profile_id':user_id,'poll_results':poll}
        return render(request, template_name="view_events.html",context=context)

def send_registration_message(event_id, user_details):
    try:
        details = Events.objects.get(id=event_id)
        Mailgun.send_mail([user_details.email], "Thankyou For showing interest!", "Thankyou For showing interest!",
                          "<p>Hi " + str(
                              user_details.username) + ",<br><br> Thankyou for registering for the event - " + str(
                              details.event_subject) + ".The Event will be held on " + str(
                              details.event_date) + " make sure you are available.<br><br> Regards,<br> Team AMS <p>")
    except Exception:
        print("Something went wrong!")

def send_creation_message(event_id):
    try:
        recievers = []
        #gather list of mails in the database
        for user in User.objects.all():
            recievers.append(user.email)
        details = Events.objects.get(id = event_id)
        details = Events.objects.get(id=event_id)
        Mailgun.send_mail(recievers, "Checkout this Event!", "Checkout this Event!",
                          "<p>Title: " + str(details.event_subject) + "<br>Event Date: " + str(
                              details.event_date) + "<br>Organizer name: " + str(
                              details.organizer_name) + "<br>Details: " + str(
                              details.text) + "<br> Venue: " + details.venue + "<br><br> please write to " + str(
                              details.email) + " in case of any queries </p>")
    except Exception:
        print("Something went wrong!")

def send_delete_notif(event_id):
    try:
        recievers = []
        #gather list of mails in the database
        for user in User.objects.all():
            recievers.append(user.email)
        details = Events.objects.get(id=event_id)
        Mailgun.send_mail(recievers, "This Event Has Been Deleted", "This Event Has Been Deleted",
                          "<p>The Below Event has been <b>Deleted</b>: <br><br> Title: " + str(
                              details.event_subject) + "<br>Event Date: " + str(
                              details.event_date) + "<br>Organizer name: " + str(
                              details.organizer_name) + "<br>Details: " + str(
                              details.text) + "<br> Venue: " + details.venue + "<br><br> please write to " + str(
                              details.email) + " in case of any queries </p>")
    except Exception:
        print("Something went wrong!")


class EventsDeleteView(View):
    def post(self,request,*args,**kwargs):
        current_date = datetime.now()
        past_events = Events.objects.filter(event_date__lt=current_date)
        past_events.delete()
        messages.warning(request, f'Past Events deleted successfully')
        return render(request,'succes.html',context={'title':'Delete Success'})

class DeleteSpecificEvent(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('event_id')
        event = Events.objects.get(id = id)
        
        # for user in Profile.objects.all():
        #     if(user.event_ids != None):
        #         jsonDec = json.decoder.JSONDecoder()
        #         ids = jsonDec.decode(user.event_ids)
        #         try:
        #             ids.remove(int(id))
        #             user.event_ids = json.dumps(ids)
        #             user.save()
        #         except Exception:
        #             print('event not present in the list')
        # send_delete_notif(id)
        event.delete()
        return HttpResponseRedirect("/view_events")
