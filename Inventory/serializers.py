from rest_framework import serializers
from .models import InventoryItem, InventoryRecord , Supplier ,OrderItem
from Doctor.models import DoctorProfile 
from decimal import Decimal
from django.utils import timezone

class AddInventorySerializer(serializers.Serializer):
    # Fields for InventoryItem
    item_name = serializers.CharField(max_length=100)
    item_description = serializers.CharField(required=False, allow_blank=True)
    category_id = serializers.IntegerField()
    supplier_id = serializers.IntegerField(required=False, allow_null=True)
    minimum_threshold = serializers.IntegerField(default=1)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all(), required=False, allow_null=True)

    # Fields for InventoryRecord
    quantity_in_stock = serializers.IntegerField()
    batch_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data):
        # Extract InventoryItem data
        item_data = {
            'name': validated_data['item_name'],
            'description': validated_data.get('item_description', ''),
            'category_id': validated_data['category_id'],
            'supplier_id': validated_data.get('supplier_id', None),
            'minimum_threshold': validated_data.get('minimum_threshold', 1),
            'cost': validated_data.get('cost', None),
            'doctor': validated_data.get('doctor_id', None)  # Link to the doctor
        }

        # Create InventoryItem
        item = InventoryItem.objects.create(**item_data)

        # Extract InventoryRecord data
        record_data = {
            'item': item,
            'quantity_in_stock': validated_data['quantity_in_stock'],
            'batch_number': validated_data.get('batch_number', ''),
            'expiration_date': validated_data.get('expiration_date', None),
        }

        # Create InventoryRecord
        inventory_record = InventoryRecord.objects.create(**record_data)

        return inventory_record



class AddSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name', 'contact_person', 'phone_number', 'email', 'address')

    def create(self, validated_data):
        # Create and return a new Supplier instance using validated data
        return Supplier.objects.create(**validated_data)\
            

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('supplier', 'item', 'doctor', 'order_date', 'time_of_order', 'expected_delivery_date',
                  'quantity_ordered', 'cost_per_item', 'total_cost', 'status', 'notes')
        read_only_fields = ('total_cost', 'order_date', 'time_of_order')  # Automatically set fields

    def create(self, validated_data):
        # Calculate the total cost
        validated_data['total_cost'] = Decimal(validated_data['quantity_ordered']) * validated_data['cost_per_item']
        
        # Auto-assign `time_of_order` and `order_date`
        if 'order_date' not in validated_data:
            validated_data['order_date'] = timezone.now().date()
        if 'time_of_order' not in validated_data:
            validated_data['time_of_order'] = timezone.now().time()
        
        # Create and return the OrderItem instance
        return OrderItem.objects.create(**validated_data)