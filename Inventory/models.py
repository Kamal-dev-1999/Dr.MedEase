from django.db import models
from django.utils import timezone
from datetime import timedelta
from Doctor.models import DoctorProfile
from decimal import Decimal

# Category model to define different item categories
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('medications', 'Medications and Pharmaceuticals'),
        ('medical_supplies', 'Medical Supplies and Consumables'),
        ('diagnostic_equipment', 'Diagnostic Equipment'),
        ('surgical_instruments', 'Surgical and Treatment Instruments'),
        ('office_supplies', 'Office Supplies and Stationery'),
        ('ppe', 'Personal Protective Equipment (PPE)'),
        ('furniture', 'Furniture and Fixtures'),
        ('medical_devices', 'Medical Devices and Equipment'),
        ('cleaning_supplies', 'Cleaning and Disinfection Supplies'),
        ('patient_support', 'Patient Comfort and Support Items'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, help_text="Description of the category")

    def __str__(self):
        return self.get_name_display()


# Supplier model for managing supplier information
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# InventoryItem model to define each item and link it to a category and supplier
# Add a ForeignKey to the DoctorProfile in InventoryItem model
class InventoryItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_items')  # Link to doctor
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    minimum_threshold = models.PositiveIntegerField(default=1, help_text="Minimum stock threshold for alerts")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Cost per item")
    
    def __str__(self):
        return f"{self.name} - {self.category} - {self.doctor if self.doctor else 'No Doctor'}"



# InventoryRecord model to manage stock levels and expiration details for each item
class InventoryRecord(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='inventory_records')
    quantity_in_stock = models.PositiveIntegerField(default=0)
    batch_number = models.CharField(max_length=50, blank=True, help_text="Batch number for tracking")
    expiration_date = models.DateField(null=True, blank=True, help_text="Expiration date for items like medications")
    added_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity_in_stock <= self.item.minimum_threshold

    def is_near_expiration(self):
        if self.expiration_date:
            return self.expiration_date <= timezone.now().date() + timedelta(days=30)
        return False

    def __str__(self):
        return f"{self.item.name} - Batch {self.batch_number} - Stock: {self.quantity_in_stock}"


class OrderItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='ordered_items')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Order date with default set to current date
    order_date = models.DateField(default=timezone.now)
    time_of_order = models.TimeField(null=True, blank=True)  # Remove auto_now_add=True
    expected_delivery_date = models.DateField(null=True, blank=True)

    # Quantity and cost fields
    quantity_ordered = models.PositiveIntegerField()
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # Status and notes fields
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    notes = models.TextField(blank=True, help_text="Additional order notes or instructions")

    def save(self, *args, **kwargs):
        # Set time_of_order to the current time if not set
        if not self.time_of_order:
            self.time_of_order = timezone.now().time()
        
        # Calculate total cost before saving
        self.total_cost = Decimal(self.quantity_ordered) * self.cost_per_item
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity_ordered} of {self.item.name} from {self.supplier.name if self.supplier else 'No Supplier'} on {self.order_date}"