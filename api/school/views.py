from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import School, Course, Lesson, Comment
from user.models import BaseUser
from .serializers import SchoolSerializer, CourseSerializer, LessonSerializer, CommentSerializer


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


# class RateLessonView(APIView):
#     """
#     Этот View проверяет, что оценка находится в диапазоне от 1 до 5, затем создает
#     или обновляет связанный объект `user_rating` для пользователя и урока.
#     После того, как оценка была добавлена, он пересчитывает средний рейтинг урока и сохраняет его
#     """
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, lesson_id):
#         lesson = get_object_or_404(Lesson, pk=lesson_id)
#         user = request.user
#         rating = float(request.data.get('rating'))
#
#         if not rating or rating < 1 or rating > 5:
#             return Response({'error': 'Invalid rating value'})
#
#         user_rating, created = BaseUser.objects.get_or_create(rated_lessons=lesson)
#         user_rating.rating = rating
#         user_rating.save()
#
#         lesson_ratings = lesson.ratings.all().values_list('rating', flat=True)
#         lesson.rating = sum(lesson_ratings) / len(lesson_ratings)
#         lesson.save()
#
#         return Response({'success': 'Lesson was rated successfully'})
#
#
# class RateCourseView(APIView):
#     """
#     Этот View проверяет, что оценка находится в диапазоне от 1 до 5, затем создает
#     или обновляет связанный объект `user_rating` для пользователя и курса.
#     После того, как оценка была добавлена, он пересчитывает средний рейтинг курса и сохраняет его
#     """
#     queryset = Course.objects.all()
#     serializer_class = LessonRateSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, course_id):
#         course = get_object_or_404(Course, pk=course_id)
#         user = request.user
#         rating = request.data.get('rating')
#
#         if not rating or rating < 1 or rating > 5:
#             return Response({'error': 'Invalid rating value'})
#
#         user_rating, created = BaseUser.objects.get_or_create(rated_courses=course)
#         user_rating.rating = rating
#         user_rating.save()
#
#         course_ratings = course.ratings.all().values_list('rating', flat=True)
#         course.rating = sum(course_ratings) / len(course_ratings)
#         course.save()
#
#         return Response({'success': 'Course was rated successfully'})
