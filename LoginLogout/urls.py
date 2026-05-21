from django.contrib import admin # Make sure this import is here!
from django.urls import path
from logger.views import log_entry, lookup_learner
from logger import views

urlpatterns = [
    path('admin/', admin.site.urls),                
    path('', log_entry, name='log_entry'),
    path('lookup/', lookup_learner, name='lookup_learner'),
    path('register-ajax/', views.register_learner_ajax, name='register_ajax'),
]