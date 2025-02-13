from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import MainCategory, SubCategory

# Create a new main category
def create_main_category(request):
    name = request.POST.get('name')
    category = MainCategory.objects.create(name=name)
    return JsonResponse({'id': category.id, 'name': category.name})

# Read all main categories
def list_main_categories(request):
    categories = MainCategory.objects.all().values()
    return JsonResponse(list(categories), safe=False)

# Update a main category
def update_main_category(request, category_id):
    category = get_object_or_404(MainCategory, id=category_id)
    category.name = request.POST.get('name')
    category.save()
    return JsonResponse({'id': category.id, 'name': category.name})

# Delete a main category
def delete_main_category(request, category_id):
    category = get_object_or_404(MainCategory, id=category_id)
    category.delete()
    return JsonResponse({'status': 'deleted'})

# CRUD for SubCategory
def create_sub_category(request):
    main_category_id = request.POST.get('main_category_id')
    product = request.POST.get('product')
    type = request.POST.get('type')
    size = request.POST.get('size')
    class_field = request.POST.get('class_field')
    face_type = request.POST.get('face_type')

    main_category = get_object_or_404(MainCategory, id=main_category_id)
    sub_category = SubCategory.objects.create(
        main_category=main_category,
        product=product,
        type=type,
        size=size,
        class_field=class_field,
        face_type=face_type
    )
    return JsonResponse({'id': sub_category.id, 'product': sub_category.product})

def list_sub_categories(request, main_category_id):
    sub_categories = SubCategory.objects.filter(main_category_id=main_category_id).values()
    return JsonResponse(list(sub_categories), safe=False)

def update_sub_category(request, sub_category_id):
    sub_category = get_object_or_404(SubCategory, id=sub_category_id)
    sub_category.product = request.POST.get('product')
    sub_category.type = request.POST.get('type')
    sub_category.size = request.POST.get('size')
    sub_category.class_field = request.POST.get('class_field')
    sub_category.face_type = request.POST.get('face_type')
    sub_category.save()
    return JsonResponse({'id': sub_category.id, 'product': sub_category.product})

def delete_sub_category(request, sub_category_id):
    sub_category = get_object_or_404(SubCategory, id=sub_category_id)
    sub_category.delete()
    return JsonResponse({'status': 'deleted'})
