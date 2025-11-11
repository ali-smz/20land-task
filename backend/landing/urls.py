from django.urls import path
from .views import SubmitView

urlpatterns = [
    path("submit/", SubmitView.as_view())
]
