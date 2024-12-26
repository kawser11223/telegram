from django.urls import path
from .views import *

urlpatterns = [
    # Other URLs
   path('',signup, name='signup'),
   
]
