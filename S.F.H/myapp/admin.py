from django.contrib import admin
from .models import *
# Register your models here.


# class productAdmin(admin.ModelAdmin):
#     list_display = ("p_name","cat_sub_two","img")
class productAdmin(admin.ModelAdmin):
    list_display =("p_name","cat_sub_two","p_size","img")

class Subcategory_twoAdmin(admin.ModelAdmin):
    list_display = ("name","cat_sub")

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name","cat")

class CartAdmin(admin.ModelAdmin):
    list_display =("user","product","status")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("user","fullname","addresstype","state")

class RegisterAdmin(admin.ModelAdmin):
    list_display =("username","useremail")

admin.site.register(Register,RegisterAdmin)
admin.site.register(Category)
admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(Subcategory_two,Subcategory_twoAdmin)
admin.site.register(Product,productAdmin)

admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Subscribe)

