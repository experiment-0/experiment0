from django.urls import path
from .views import SchoolListView, SingleSchoolView, AdminsSchoolView, CourseListView, SingleCourseView, \
    StudentsCoursesView, LessonListView, SingleLessonView, CoursesLessonsView, ListCreateCommentsView, \
    CommentDetailView

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
    # path('courses/lessons/<int:lesson_id>/rate/', RateLessonView.as_view(), name='lesson-rate'),
    # path('courses/<int:lesson_id>/rate/', RateCourseView.as_view(), name='course-rate'),
]
