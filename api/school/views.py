from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import School, Course, Lesson, Comment, Rating
from user.models import BaseUser
from .serializers import SchoolSerializer, CourseSerializer, LessonSerializer, \
    CommentSerializer, RatingSerializer


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


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Comment по его идентификатору, и позволит получить/редактировать/удалить данный комментарий
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)


class ListCreateCommentsView(APIView):
    """
    все комментарии для определённого урока и создаст новый комментарий, связывая его создателя (request.user) с уроком
    (по его идентификатору lesson_id).
    {
    "text": "text_comment",
    "user": user_id,
    "lesson": lesson_id
    }
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, lesson_id):
        comments = Comment.objects.filter(lesson=lesson_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, lesson_id):
        print(request, lesson_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, lesson_id=lesson_id)
        return Response(serializer.data)


class RatingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Обновление и удаление оценки определенного урока от юзера
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonRatingAPIView(generics.RetrieveAPIView, generics.CreateAPIView):
    """
    Возможность для юзера один раз поставить оценку и отображение средней оценки определенного урока
    """

    serializer_class = RatingSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Lesson, pk=kwargs.get("pk"))
        rating = instance.rating if instance.ratings.exists() else 0
        return Response({"rating": rating})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
