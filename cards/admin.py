from django.contrib import admin
from .models import Category, Card, Rating, User, Comment, LessionView, Tag,Order,OrderItem, UserPublic, Socials, Emails, Phones, CardPreview, Contact, BackGroudCard, Data2, Data3


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Card)
admin.site.register(Tag)
# admin.site.register(Action)
admin.site.register(LessionView)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CardPreview)
admin.site.register(Contact)
admin.site.register(BackGroudCard)

admin.site.register(Phones)
admin.site.register(Emails)
admin.site.register(Socials)

admin.site.register(Data2)
admin.site.register(Data3)
admin.site.register(UserPublic)
