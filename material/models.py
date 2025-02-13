from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)  # MainCategory name is required

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories')
    product = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    class_field = models.CharField(max_length=255)  # Renamed 'class' to 'class_field' to avoid conflict with Python keywords
    face_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product} ({self.type}, {self.size}, {self.class_field}, {self.face_type})"
