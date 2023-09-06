from .models import Category, Card, Tag, Rating, User, Comment, LessionView, Order, OrderItem, UserPublic, CardPreview, Contact, BackGroudCard, UserPublic, Data2, Data3
from .serializers import CategorySerializer, CardSerializer, CardDetailSerializer, RatingSerializer, UserSerializer , CommentSerializer, LessonViewSerializer, MyOrderSerializer, MyPublicUserSerializer, CardPreviewSerializer, ContactSerializer, ChangePasswordSerializer, UpdateUserSerializer, BackGroudCardSerializer, PublicUserSerializer
from .paginator import BasePaginator

from django.http import Http404
from django.conf import settings
from django.db.models import F
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status, permissions, authentication
from rest_framework.decorators import action
from rest_framework.response import Response


from PIL import Image, ImageFont, ImageDraw, ImageFilter
import openpyxl

from django.core.files import File as DjangoFile

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

import os

from rest_framework_simplejwt.tokens import RefreshToken

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class  = CategorySerializer

class ContactViewSet(viewsets.ViewSet):
    serializer_class  = ContactSerializer

    @action(methods=['post'], detail=False, url_path="add_contact")
    def add_card(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages="Cảm ơn bạn đã đóng góp"
            return Response(messages,status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CardViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = CardSerializer
    pagination_class = BasePaginator

    def get_queryset(self):
        cards = Card.objects.filter(active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            cards = cards.filter(name__icontains=q)
        
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            cards = cards.filter(category_id=cate_id)

        return cards

    def get_permissions(self):
        if self.action in ['add_comment', 'add_card', 'rate', 'preview_card']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path="add_card")
    def add_card(self, request, format=None):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path="preview_card")
    def preview_card(self, request, pk):
        serializer = CardPreviewSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            hovaten = data['name']
            title = data['title']
            link = data['link']
            card = self.get_object()

            text1 = (int(card.lo_titleTruoc.split(",")[0]), int(card.lo_titleTruoc.split(",")[1]))
            color1= (int(card.lo_rgbtitleTruoc.split(",")[0]), int(card.lo_rgbtitleTruoc.split(",")[1]), int(card.lo_rgbtitleTruoc.split(",")[2]))
            text2 = (int(card.lo_nameTruoc.split(",")[0]), int(card.lo_nameTruoc.split(",")[1]))
            color2= (int(card.lo_rgbnameTruoc.split(",")[0]), int(card.lo_rgbnameTruoc.split(",")[1]), int(card.lo_rgbnameTruoc.split(",")[2]))
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=2,
            )
            qr.add_data(data['link'])
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save('qr.png')


            my_background_truoc = Image.open(card.imageTruoc)
            text_font = ImageFont.truetype('temp/Montserrat_seminobold.TTF', 45)

            my_background_sau = Image.open(card.imageSau)
            text_font = ImageFont.truetype('temp/Montserrat_seminobold.TTF', 45)

            text_hoten = hovaten
            text_title = title

            # Truoc
            image_editable = ImageDraw.Draw(my_background_truoc)
            image_editable.text(text1, text_hoten,color1, font = text_font)
            image_editable.text(text2, text_title,color2, font = text_font)
            my_background_truoc.save("temp/"+ str(title) + "_truoc.png")

            m1t =Image.open("temp/"+ str(title) + "_truoc.png")
            m2t = Image.open('qr.png')
            m2t = m2t.resize((100,100))
            m1t.paste(m2t,(400, 100))
            m1t.save("temp/"+ str(title) + "_truoc.png")
            # Truoc

            # Sau
            image_editable_sau = ImageDraw.Draw(my_background_sau)
            image_editable_sau.text(text1, text_hoten,color1, font = text_font)
            image_editable_sau.text(text2, text_title,color2, font = text_font)
            my_background_sau.save("temp/"+ str(title) + "_sau.png")

            m1s =Image.open("temp/"+ str(title) + "_sau.png")
            m2s = Image.open('qr.png')
            m2s = m2s.resize((100,100))
            m1s.paste(m2s,(400, 100))
            m1s.save("temp/"+ str(title) + "_sau.png")
            # Sau

            file_obj1 = DjangoFile(open("temp/"+ str(title) + "_truoc.png", mode='rb'), name="temp/"+ str(title) + "_truoc.png")
            file_obj2 = DjangoFile(open("temp/"+ str(title) + "_sau.png", mode='rb'), name="temp/"+ str(title) + "_sau.png")
            serializer = CardPreview.objects.create(title=text_title, name=text_hoten, link=link, imageTruoc=file_obj1,imageSau=file_obj2 , card=self.get_object(), creator = request.user)
            # print("Đã tạo: " + str(title))
            os.remove("temp/"+ str(title) + "_truoc.png")
            os.remove("temp/"+ str(title) + "_sau.png")

            return Response(CardPreviewSerializer(serializer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['post'], detail=True, url_path="tags")
    def add_tag(self, request, pk):
        try:
            card = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get("tags")
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    card.tags.add(t)
                
                card.save()
                return Response(self.serializer_class(card).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    
    @action(methods=['post'], detail=True, url_path="rating")
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating, creator= request.user, card=self.get_object())

            return Response(RatingSerializer(r).data, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
           c = Comment.objects.create(content=content, card=self.get_object(), creator= request.user)
           return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
    @action(methods=['get'], detail=True, url_path="views")
    def inc_view(self, request, pk):
        v, created = LessionView.objects.get_or_create(card = self.get_object())
        v.view += 1
        v.save()
        v.refresh_from_db()
        return Response(LessonViewSerializer(v).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="comment")
    def get_comment(self, request, pk):
        c = Comment.objects.filter(card = self.get_object())
        serializer = CommentSerializer(c, many=True)
        print(c)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = BasePaginator
    permission_class  = [permissions.IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            print(request.data)
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

class CardPreviewViewSet(viewsets.ViewSet,  generics.DestroyAPIView):
    queryset = CardPreview.objects.all()
    serializer_class = CardPreviewSerializer
    pagination_class = BasePaginator
    permission_class  = [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=False, url_path="views")
    def get_cardpreviews(self, request, format=None):
        cardpreviews = CardPreview.objects.filter(creator=request.user)
        serializer = CardPreviewSerializer(cardpreviews, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class  = UserSerializer

    def get_permissions(self):
        if self.action in ['get_current_user', 'orders']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     partial = True # Here I change partial to True
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     if serializer.is_valid():
    #         print(set_password(request.data['password']))
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)

    # def patch(self, request):
    #     serialized = UserSerializer(data=request.DATA)
    #     if serialized.is_valid():
    #         serialized.save()
    #         return Response(status=status.HTTP_205_RESET_CONTENT)
    #     else:
    #         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileView(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OUTH2_INFO, status=status.HTTP_200_OK)

# class OrdersList(APIView):
#     permission_class  = [permissions.IsAuthenticated()]

#     def get(self, request, format=None):
#         orders = Order.objects.filter(user=request.user)
#         serializer = MyOrderSerializer(orders, many=True)
#         return Response(serializer.data)


class OrdersList(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class  = MyOrderSerializer

    def get_permissions(self):
        if self.action in ['add_order', 'get_order']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path="add_order")
    def add_order(self, request):
        serializer = MyOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False, url_path="views")
    def get_order(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path="detail_pages")
    def get_queryset(self, request):
        orders = Order.objects.all()
        orde_id = self.request.query_params.get('order_id')
        print(orde_id)
        if orde_id is not None:
            orders = orders.filter(id=orde_id)
        serializer = MyOrderSerializer(orders, many=True)
        # return orders
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    


# class OrdersList(viewsets.ViewSet, generics.RetrieveAPIView):
#     queryset = Order.objects.all()
#     serializer_class  = MyOrderSerializer
#     permission_class  = [permissions.IsAuthenticated()]

#     def get_permissions(self):
#         if self.action == 'get_order':
#             return [permissions.IsAuthenticated()]
        
#         return [permissions.AllowAny()]

#     def get_order(self, request, format=None):
#         orders = Order.objects.filter(user=request.user)
#         serializer = MyOrderSerializer(orders, many=True)
#         return Response(serializer.data)

# class OrdersList(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         orders = Order.objects.filter(user=request.user)
#         serializer = MyOrderSerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)




class UserPublicViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = UserPublic.objects.all()
    serializer_class  = PublicUserSerializer

    def get_permissions(self):
        if self.action in ['create_publicuser', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path="create_publicuser")
    def create_publicuser(self, request):
        userpublics = UserPublic.objects.all()
        serializer = PublicUserSerializer(data=request.data)
        print(request.data)
        if (serializer.is_valid()):
            serializer.save(username=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().username:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=False, url_path="views")
    def get_user(self, request, format=None):
        userpublics = UserPublic.objects.all()
        q = self.request.query_params.get('q')
        if q is not None:
            userpublic = userpublics.filter(username = q)
        serializer = PublicUserSerializer(userpublic, many=True)
        return Response(serializer.data)



class BackGroudCardSerializer(viewsets.ViewSet, generics.ListAPIView):
    queryset = BackGroudCard.objects.all()
    serializer_class = BackGroudCardSerializer
    pagination_class = BasePaginator



# class UserPublicViewSet(viewsets.ViewSet, generics.UpdateAPIView):
#     queryset = UserPublic.objects.all()
#     serializer_class  = MyPublicUserSerializer

#     def get_permissions(self):
#         if self.action in ['create_publicuser', 'partial_update']:
#             return [permissions.IsAuthenticated()]
#         return [permissions.AllowAny()]

#     @action(methods=['post'], detail=False, url_path="create_publicuser")
#     def create_publicuser(self, request):
#         userpublics = UserPublic.objects.all()
#         serializer = MyPublicUserSerializer(data=request.data)

#         if (serializer.is_valid() and UserPublic.objects.filter(user=request.user).count() == 0):
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, *args, **kwargs):
#         if request.user == self.get_object().user:
#             return super().partial_update(request, *args, **kwargs)
#         return Response(status=status.HTTP_403_FORBIDDEN)

#     @action(methods=['get'], detail=False, url_path="views")
#     def get_user(self, request, format=None):
#         userpublics = UserPublic.objects.all()
#         q = self.request.query_params.get('q')
#         if q is not None:
#             userpublic = userpublics.filter(username = q)
#         serializer = MyPublicUserSerializer(userpublic, many=True)
#         return Response(serializer.data)