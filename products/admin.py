from django.contrib import admin
from .models import Category, Products,ProductsImage, Comment


class ProductsImageAdmin(admin.TabularInline):
    model = ProductsImage



class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'author', 'date']
    inlines = [ProductsImageAdmin]


admin.site.register(Category)
admin.site.register(ProductsImage)
admin.site.register(Products, ProductAdmin)
admin.site.register(Comment)
