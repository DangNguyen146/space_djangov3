from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import User, Category, Card, Tag, Rating, Comment, LessionView, Order, OrderItem, UserPublic, Phones, Emails, Socials, CardPreview, Contact, BackGroudCard, UserPublic, Data2, Data3
from django.contrib.auth.password_validation import validate_password
from django.db.models import CharField
from django.contrib.auth.hashers import make_password

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ["id", "name", "image", "imageTruoc", "imageSau", "price", "description", "created_date", "category"]

    def create(seft, validated_data):
        card = Card.objects.create(**validated_data)
        return card

class CardPreviewSerializer(ModelSerializer):
    class Meta:
        model = CardPreview
        fields = ["id", "title", "name", "link", "imageTruoc", "imageSau", "card", "creator"]
    
    def create(seft, validated_data):
        cardp = CardPreview.objects.create(**validated_data)
        return cardp

class CardDetailSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = CardSerializer.Meta.model
        fields =  CardSerializer.Meta.fields + ['tags']



class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rate", "created_date"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id" ,"avatars", "first_name", "last_name", "username", "password", "email", "date_joined"]
        extra_kwargs = {
            'password' : {'write_only': 'true'}
        }

    def create(self, validated_data):
        user=User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for f in UserSerializer.Meta.fields + UserSerializer.Meta.write_only_fields:
            set_attr(instance, f, validated_data[f])
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance

class CommentSerializer(ModelSerializer):
    creator = UserSerializer()
    class Meta:
        model = Comment
        fields = ["id", "content", "creator", "created_date", "update_date"]



class LessonViewSerializer(ModelSerializer):
    class Meta:
        model = LessionView
        fields = ['id', 'view', 'card']


class MyOrderItemSerializer(ModelSerializer):
    # card = CardSerializer()
    class Meta:
        model = OrderItem
        fields = ["price", "card", "quantity"]

class MyOrderSerializer(ModelSerializer):
    items = MyOrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["id", "first_name", "last_name","email", "address","place","phone", "type","items"]

    def create(seft, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order


class MyPublicUserPhonesSerializer(ModelSerializer):
    class Meta:
        model = Phones
        fields = ["name", "phone", "description"]

class MyPublicUserEmailsSerializer(ModelSerializer):
    class Meta:
        model = Emails
        fields = ["name", "email", "description"]

class MyPublicUserSocialsSerializer(ModelSerializer):
    class Meta:
        model = Socials
        fields = ["name", "image", "link", "description"]

class MyPublicUserSerializer(ModelSerializer):
    phones = MyPublicUserPhonesSerializer(many=True)
    emails = MyPublicUserEmailsSerializer(many=True)
    socials = MyPublicUserSocialsSerializer(many=True)

    class Meta:
        model = UserPublic
        fields = ["id", "username", "fullname", "cover","phones", "emails","socials"]

    def create(seft, validated_data):
        items_phone = validated_data.pop('phones')
        items_email = validated_data.pop('emails')
        items_social = validated_data.pop('socials')
        userpublic = UserPublic.objects.create(**validated_data)

        for item_data in items_phone:
            Phones.objects.create(user=userpublic, **item_data)
        
        for item_data in items_email:
            Emails.objects.create(user=userpublic, **item_data)

        for item_data in items_social:
            Socials.objects.create(user=userpublic, **item_data)
            
        return userpublic


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "email", "title", "message"]


class BackGroudCardSerializer(ModelSerializer):
    class Meta:
        model = BackGroudCard
        fields = ["id", "title", "css", "image"]

class Data2Serializer(ModelSerializer):
    class Meta:
        model = Data2
        fields = ["title", "link"]

class Data3Serializer(ModelSerializer):
    class Meta:
        model = Data3
        fields = ["profile_title", "decripttion"]

class PublicUserSerializer(ModelSerializer):
    # data2 = Data2Serializer(many=True)
    # data3 = Data3Serializer(many=True)
    class Meta:
        model = UserPublic
        fields = ["username","avatars", "profile_title","decripttion", "data", "css"]
        
    def create(seft, validated_data):
        # items_data2 = validated_data.pop('data2')
        userpublic = UserPublic.objects.create(**validated_data)
        # for item_data in items_data2:
        #     Data2.objects.create(username=userpublic, **item_data)
            
        return userpublic

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        
        instance.username = validated_data['username']
        instance.avatars = validated_data['avatars']
        data2 = validated_data.pop('data2')
        
        instance.save()
        
        return instance