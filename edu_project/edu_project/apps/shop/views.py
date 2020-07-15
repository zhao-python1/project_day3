import logging

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_redis import get_redis_connection
from rest_framework import status
from course.models import Course
from rest_framework.permissions import IsAuthenticated

from edu_project.settings import constants
from edu_project.settings.constants import IMAGE_SRC

logs = logging.getLogger("django")


class ShopView(ViewSet):
    permission_classes = [IsAuthenticated]
    '''购物相关的处理
    用户id 课程id 有效期 勾选状态
    '''

    def add_shop(self, request):
        # 课程id
        course_id = request.data.get('course_id')
        # 用户id
        user_id = request.user.id
        # 是否勾选
        select = True

        # 有效期
        expire = 0

        # 检验前端提交的参数

        try:
            Course.objects.get(is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取redis连接对象
            redis_connection = get_redis_connection("cart")
            # 将数据保存到redis
            pipeline = redis_connection.pipeline()
            # 管道开启
            pipeline.multi()
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 被勾选的商品
            pipeline.sadd("selected_%s" % user_id, course_id)
            # 执行
            pipeline.execute()
            course_len = redis_connection.hlen("cart_%s" % user_id)

        except:
            logs.error("购物车数据储存失败")
            return Response({"message": "参数有误，购物车添加失败"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({"message": "购物车商品添加成功", "cart_length": course_len})

    def list_cart(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        cart_list_bytes = redis_connection.hgetall('cart_%s' % user_id)
        select_list_bytes = redis_connection.smembers("selected_%s" % user_id)
        # print("cart_list",cart_list)
        # print("select_list",select_list)
        # 循环从mysql找出商品
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                # 获取到的所有的课程信息
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            # 将购物车所需的信息返回
            data.append({
                "selected": True if course_id_byte in select_list_bytes else False,
                "course_img": constants.IMAGE_SRC + course.course_img.url,
                "name": course.name,
                "id": course_id,
                "expire_id": expire_id,
                "price": course.price,
            })

        return Response(data)

    def change_select(self, request):
        '''切换购物车状态'''
        user_id = request.user.id
        selected = request.data.get('selected')
        course_id = request.data.get('course_id')
        try:
            # 获取到的所有的课程信息
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，当前商品不存在"}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection('cart')
        if selected:
            # 讲商品添加到 set 代表选中
            redis_connection.sadd("selected_%s" % user_id, course_id)
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)

        return Response({"message": "状态相同，切换成功"}, status=status.HTTP_400_BAD_REQUEST)


    def delete_cart(self, request):
        '''删除购物车信信息'''
        user_id = request.user.id
        course_id = request.data.get('course_id')
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数传递错误，没有相关课程'}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection('cart')
        if course_id:
            redis_connection.hdel('cart_%s' % user_id, course_id)
        return Response({'message': '删除成功'}, status=status.HTTP_200_OK)

