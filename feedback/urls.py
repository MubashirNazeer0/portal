from django.urls import path

from .views import *

urlpatterns =[
    path(r'feedback/', FeedbackView.as_view(), name="feedback_home"),
    path(r'view/', ViewAllFeedback.as_view(), name="view_feedback"),
    path(r'view/<str:cat>', ViewAllFeedback.as_view(), name="view_cat_feedback"),
    path(r'feedback/delete', ClearFeedbackView.as_view(), name="clear_feedback"),
]