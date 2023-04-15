from django.urls import path
from .views import SchoolListView, SingleSchoolView

urlpatterns = [
    path('schools/', SchoolListView.as_view(), name='school-list'),
    path('schools/<int:pk>', SingleSchoolView.as_view(), name='school-details'),
]
