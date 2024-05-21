from django.urls import path
from .views.process_file_view import ProcessFileView
from .views.retrieve_row_view import RetrieveRowsView

urlpatterns = [
    path('processFile/', ProcessFileView.as_view(), name='processFile'),
    path('retrieveRows/', RetrieveRowsView.as_view(), name='retrieveRows'),
]
