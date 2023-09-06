from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatars = models.ImageField(upload_to='uploads/%Y/%m', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    


class UserPublic(models.Model):
    username = models.CharField(max_length=100,  blank=True, null=True)
    avatars = models.ImageField(upload_to='uploads/%Y/%m', blank=True, null=True)
    profile_title =   models.CharField(max_length=250, null=False)
    decripttion = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    css = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='background/%Y/%m', default=None,  blank=True, null=True)

class Data2(models.Model):
    username = models.ForeignKey(UserPublic, related_name='data2', on_delete=models.CASCADE)
    title =  models.CharField(max_length=250, null=True)
    link =  models.CharField(max_length=250, null=True)


class Data3(models.Model):
    username = models.ForeignKey(UserPublic, related_name='data3', on_delete=models.CASCADE)
    # avatars = models.ImageField(upload_to='uploads/%Y/%m', blank=True, null=True)
    profile_title =   models.CharField(max_length=250, null=False)
    decripttion = models.TextField(null=True, blank=True)
    
    
class Phones(models.Model):
    user = models.ForeignKey(UserPublic, related_name='phones', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class Emails(models.Model):
    user = models.ForeignKey(UserPublic, related_name='emails', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class Socials(models.Model):
    FACEBOOK, INSTAGRAM, TIKTOK, TWITTER, ZALO, DEFAULT = range(6)
    STATUS =[
        (FACEBOOK,'facebook'),
        (INSTAGRAM,'instagram'),
        (TIKTOK,'tiktok'),
        (TWITTER,'twitter'),
        (ZALO,'zalo'),
        (DEFAULT,'khac')
    ]

    user = models.ForeignKey(UserPublic, related_name='socials', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    image =  models.ImageField(upload_to='uploads/social', blank=True, null=True)
    link = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id


class Category(models.Model):
    name = models.CharField(max_length=100, null=False,unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class MyModelBase(models.Model):
    name = models.CharField(max_length=250, null=False)
    image = models.ImageField(upload_to='cards/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Card(MyModelBase):
    class Meta:
        unique_together = ('name', 'category')
        ordering = ["-id"]

    lo_titleTruoc = models.TextField(default="300,300", null=True, blank=True)
    lo_rgbtitleTruoc = models.TextField(default="0,0,0", null=True, blank=True)
    lo_nameTruoc = models.TextField(default="200,200", null=True, blank=True)
    lo_rgbnameTruoc = models.TextField(default="228,178,149", null=True, blank=True)




    imageTruoc = models.ImageField(upload_to='cards/%Y/%m', default=None, null=True, blank=True)
    imageSau = models.ImageField(upload_to='cards/%Y/%m', default=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField("Tag", related_name="cards", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)

class CardPreview(models.Model):
    title =  models.CharField(max_length=250, null=False)
    name =  models.CharField(max_length=250, null=False)
    link =  models.CharField(max_length=250, null=False)
    imageTruoc = models.ImageField(upload_to='cards/%Y/%m', default=None, null=True, blank=True)
    imageSau = models.ImageField(upload_to='cards/%Y/%m', default=None, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    creator = models.ForeignKey(User,null=True, blank=True, on_delete= models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class ActionBase(models.Model):
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(Card, on_delete= models.CASCADE)
    
    class Meta:
        abstract = True # Lớp trừu tượng


class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)


class LessionView(models.Model):
    view = models.IntegerField(default=0)
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

class Order(models.Model):
    GIOHANG, DANGXULY, DANGGIAO = range(3)
    STATUS =[
        (GIOHANG,'giohang'),
        (DANGXULY,'dangxuLi'),
        (DANGGIAO,'danggiao')
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    type = models.PositiveSmallIntegerField(choices=STATUS, default=GIOHANG)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id


class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    title = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title


class BackGroudCard(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    css = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='background/%Y/%m', default=None,  blank=True, null=True)
    def __str__(self):
        return self.title