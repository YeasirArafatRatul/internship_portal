# from django import template
# from django.db.models import Sum
# from django.urls import reverse


# from order.models import ShopCart
# from store.models import Category

# register = template.Library()


# @register.simple_tag
# def categorylist():
#     return Category.objects.all()


# @register.simple_tag
# def shopcartcount(userid):
#     count = ShopCart.objects.filter(user_id=userid).count()
#     return count
