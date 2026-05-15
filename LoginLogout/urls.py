from django.contrib import admin # Make sure this import is here!
from django.urls import path
from logger.views import log_entry, lookup_learner

urlpatterns = [
    path('admin/', admin.site.urls),                # This line was missing!
    path('', log_entry, name='log_entry'),
    path('lookup/', lookup_learner, name='lookup_learner'),
]