import xadmin

from course.models import Course, CourseCategory, CourseLesson, CourseChapter, Teacher


# 课程分类表
class CourseCateModelAdmin(object):
    pass


xadmin.site.register(CourseCategory, CourseCateModelAdmin)


# 课程信息表
class CourseModelAdmin(object):
    pass


xadmin.site.register(Course, CourseModelAdmin)


# 课程课时表
class CourseLessonModelAdmin(object):
    pass


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


# 课程章节表
class CourseChapterModelAdmin(object):
    pass


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


# 教师表
class TeacherModelAdmin(object):
    pass


xadmin.site.register(Teacher, TeacherModelAdmin)
