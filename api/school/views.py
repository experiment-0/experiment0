from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import School
from user.models import BaseUser
from .serializers import SchoolSerializer


class SchoolListView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school_admin = get_object_or_404(BaseUser, id=self.request.data.get('school_admin'))
        if school_admin.role != 'SA':
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SingleSchoolView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
