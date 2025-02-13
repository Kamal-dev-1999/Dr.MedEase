from django.urls import path
from . import views

urlpatterns = [
    # MainCategory CRUD
    path('main-category/create/', views.create_main_category, name='create_main_category'),
    path('main-category/', views.list_main_categories, name='list_main_categories'),
    path('main-category/update/<int:category_id>/', views.update_main_category, name='update_main_category'),
    path('main-category/delete/<int:category_id>/', views.delete_main_category, name='delete_main_category'),

    # SubCategory CRUD
    path('sub-category/create/', views.create_sub_category, name='create_sub_category'),
    path('sub-category/<int:main_category_id>/', views.list_sub_categories, name='list_sub_categories'),
    path('sub-category/update/<int:sub_category_id>/', views.update_sub_category, name='update_sub_category'),
    path('sub-category/delete/<int:sub_category_id>/', views.delete_sub_category, name='delete_sub_category'),
]
