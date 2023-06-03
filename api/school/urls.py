from django.urls import path
from .views import SchoolListView, SingleSchoolView, AdminsSchoolView, \
    CourseListView, SingleCourseView, \
    StudentsCoursesView, LessonListView, SingleLessonView, CoursesLessonsView, \
    ListCreateCommentsView, \
    CommentDetailView, LessonRatingAPIView, RatingRetrieveUpdateDestroyAPIView, \
    complete_lesson, OpenedLessonsView

urlpatterns = [
    path('schools/', SchoolListView.as_view(), name='school-list'),
    path('schools/<int:pk>', SingleSchoolView.as_view(), name='school-details'),
    path('admin_schools/', AdminsSchoolView.as_view(), name='admin_schools'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>', SingleCourseView.as_view(), name='course-details'),
    path('students_courses/', StudentsCoursesView.as_view(), name='students-courses'),
    path('courses/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('courses/lessons/<int:pk>', SingleLessonView.as_view(), name='lesson-details'),
    path('courses/<int:course_id>/lessons/courses_lessons/', CoursesLessonsView.as_view(), name='courses-lessons'),
    path('lessons/<int:lesson_id>/comments/', ListCreateCommentsView.as_view(), name='comments-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path("lesson/<int:pk>/rating/", LessonRatingAPIView.as_view(),
         name="lesson-rating"),
    path("rating/<int:pk>/", RatingRetrieveUpdateDestroyAPIView.as_view(),
         name="rating-retrieve-update-delete"),
    path('complete_lesson/<int:student_id>/<int:lesson_id>/', complete_lesson, name='complete_lesson'),
    path('complete_lesson/', OpenedLessonsView.as_view(), name='complete_user_lesson'),
]
