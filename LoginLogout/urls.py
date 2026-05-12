from django.contrib import admin
from django.urls import path
from logger.views import log_entry  # This imports the view we wrote

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', log_entry, name='log_entry'), # This tells Django to show our form on the home page
]