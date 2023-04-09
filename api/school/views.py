from rest_framework import generics, status
from rest_framework.generics import get_object_or_404

from .models import School
from user.models import SchoolAdmin
from .serializers import SchoolSerializer


class SchoolListView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def perform_create(self, serializer):
        school_admin = get_object_or_404(SchoolAdmin, id=self.request.data.get('id'))
        return serializer.save(school_admin=school_admin)


class SingleSchoolView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
