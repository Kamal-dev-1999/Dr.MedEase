from django.contrib import admin
from .models import MainCategory, SubCategory

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_category', 'product', 'type', 'size', 'class_field', 'face_type')
