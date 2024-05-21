from .views.process_file_view import ProcessFileView
from django.urls import path

urlpatterns = [
    path('processFile/', ProcessFileView.as_view(), name='processFile'),
]
