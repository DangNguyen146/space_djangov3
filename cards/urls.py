from django.urls import path, include
from rest_framework import routers
from . import views


routers = routers.DefaultRouter()
routers.register("categories", views.CategoryViewSet, 'category')
routers.register("cards", views.CardViewSet, 'card')
routers.register("backgrounds", views.BackGroudCardSerializer, 'background')
routers.register("users", views.UserViewSet, 'user')
routers.register("comments", views.CommentViewSet, 'comment')
routers.register("orders", views.OrdersList, 'order')
routers.register("userviews", views.UserPublicViewSet, 'userview')
routers.register("cardpreviews", views.CardPreviewViewSet, 'cardpreview')
routers.register("contacts", views.ContactViewSet, 'contact')
routers.register("changepasswords", views.ChangePasswordView, 'changepassword')
routers.register("updateusers", views.UpdateProfileView, 'updateuser')

urlpatterns = [
    path('', include(routers.urls)),
    path('oauth2-info/', views.AuthInfo.as_view()),
    # path('orders/', views.OrdersList.as_view())
]