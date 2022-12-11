from django.contrib import admin
from .models import Product, Category,Image, Rating


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']

admin.site.register(Product, ProductAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['img', 'product']
admin.site.register(Image, ImageAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['rating', 'product']
admin.site.register(Rating, RatingAdmin)