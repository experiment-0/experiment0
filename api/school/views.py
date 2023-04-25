from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import School, Course, Lesson
from user.models import BaseUser
from .serializers import SchoolSerializer, CourseSerializer, LessonSerializer


class SchoolListView(generics.ListCreateAPIView):
    """
    Список всех онлайн-школ. Создание школы (если роль SchoolAdmin)
    """
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
    """
    Редактирование школы по id
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated, )


class AdminsSchoolView(generics.ListAPIView):
    """
    Список школ для админа школы (видит только созданные им школы)
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return School.objects.filter(school_admin=user_id)


class CourseListView(generics.ListCreateAPIView):
    """
    Список всех курсов. Создание курса (доступ только авторизованному)
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SingleCourseView(generics.RetrieveAPIView):
    """
    Редактирование курса по id
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )


class StudentsCoursesView(generics.ListAPIView):
    """
    Список приобретенных курсов (связь студент-курс)
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        return Course.objects.filter(user=user_id)


class LessonListView(generics.ListCreateAPIView):
    """
    Список всех уроков. Создание урока (доступ только авторизованному)
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SingleLessonView(generics.RetrieveAPIView):
    """
    Редактирование урока по id
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, )


class CoursesLessonsView(generics.ListAPIView):
    """
    Уроки конкретного курса доступные студенту (если студент приобрел курс)
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        course_id = self.kwargs.get(
            'course_id')
        return Lesson.objects.filter(course=course_id,
                                     course__user=user_id)

