from django.urls import path

from shop import views

urlpatterns = [
    # path("banner/", views.BannerListAPIView.as_view()),
    # path("nav/", views.BannerListAPIViews.as_view()),
    path("shopping/", views.ShopView.as_view({"post":"add_shop",
                                              "get":"list_cart",
                                              "patch":"change_select",
                                              "delete":"delete_cart"})),
]