from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from course.models import CourseCategory, Course, CourseLesson, CourseChapter
from course.serializer import CourseCategorySerializer, CourseLessonModelSerializer, CourseCapterModelSerializer
from course.serializer import CourseModelSerializer

from course.pagination import CoursePageNumber



class CourseCatgoryListAPIView(ListAPIView):
    '''
    课程分类信息查询
    '''
    queryset = CourseCategory.objects.filter(is_show=True,is_delete=False).order_by("orders")
    serializer_class = CourseCategorySerializer


class CourseListAPIView(ListAPIView):
    """课程列表查询"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer




class CourseFilterListAPIView(ListAPIView):
    '''根据条件查询课程'''

    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer

    #根据不同的分类信息查询讯息 查不同的课程
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    lookup_field = ("course_category")

    #排序
    ordering_fields = ("id", "students","price")

    # 分页 只能有一个
    pagination_class = CoursePageNumber




class CourseLessonListAPIView(RetrieveAPIView):
    '''查询单个课程信息'''
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders","-id")
    serializer_class = CourseLessonModelSerializer
    lookup_field = 'id'


class CourseCapterAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True,is_delete=False).order_by("orders","id")
    serializer_class = CourseCapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']

