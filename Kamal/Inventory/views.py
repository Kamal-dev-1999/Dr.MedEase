from django.core.exceptions import ObjectDoesNotExist
from .models import Supplier, Category, DoctorProfile , InventoryRecord ,InventoryItem , OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddInventorySerializer , AddSupplierSerializer , OrderSerializer
from django.shortcuts import render , redirect 
from django.contrib import messages
from django.views import View

class AddInventoryView(APIView):
    
    def get(self, request):
        if request.user.is_anonymous:
            return render(request,'marketplace/signin.html', {'error': 'Please log in to add inventory.'})
        # Fetch all suppliers
        suppliers = Supplier.objects.all()
        categories = Category.objects.all()

        # # Render a template or return a response with suppliers and categories
        # return render(request, 'your_template.html', {'suppliers': suppliers, 'categories': categories})
            
            # Render the HTML template for the form and pass suppliers data
        return render(request, 'inventory/add_inventory.html', {'suppliers': suppliers , 'categories':categories})
    
    def post(self, request):
        # Get the logged-in doctor's profile
        doctor = None
        try:
            doctor = DoctorProfile.objects.get(user=request.user)  # Assuming the logged-in user is a doctor
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Logged-in user is not associated with a doctor profile"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data for serialization
        data = request.data.copy()  # Make a copy of the data to modify
        data['doctor_id'] = doctor.id  # Add the logged-in doctor's ID automatically

        # Pass the data to the serializer
        serializer = AddInventorySerializer(data=data)

        if serializer.is_valid():
            try:
                # Ensure category_id and supplier_id exist
                category = Category.objects.get(id=data['category_id'])
                if 'supplier_id' in data and data['supplier_id']:
                    supplier = Supplier.objects.get(id=data['supplier_id'])
                else:
                    supplier = None
                
                # Save the inventory record with the logged-in doctor
                inventory_record = serializer.save(doctor=doctor, supplier=supplier)

                messages.success(request, "Inventory added successfully!")
                return redirect('Inventory:view_inventory')

            except ObjectDoesNotExist as e:
                return Response({"error": f"Invalid foreign key reference: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddSellerView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request,'marketplace/signin.html', {'error': 'Please log in to add seller.'})
        return render(request, 'inventory/add_seller.html')
    
    def post(self, request):
        # Get the logged-in doctor's profile
        try:
            doctor = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            messages.error(request, "Logged-in user is not associated with a doctor profile.")
            return redirect('Inventory:add_seller')  # Redirect back to the form with error message

        # Prepare data for serialization
        data = request.POST.copy()
        data['doctor_id'] = doctor.id

        # Initialize the serializer
        serializer = AddSupplierSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Supplier added successfully!")
            return redirect('Inventory:add_seller')  # Redirect to the same page to show success message
        else:
            messages.error(request, "There was an error adding the supplier.")
            return render(request, 'inventory/add_seller.html', {'errors': serializer.errors})

                
class ViewInventory(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request,'marketplace/signin.html', {'error': 'Please log in to view inventory.'})
        # Fetch all inventory records
        inventories = InventoryRecord.objects.all()
        
        if inventories.exists():
            # Render template if inventory records are found
            return render(request, 'inventory/view_inventory.html', {'inventories': inventories})
        
        # Return a JSON response if no inventory records are found
        return render(request, 'inventory/view_inventory.html', {'inventories': inventories})
        
        
class AddOrderView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request,'marketplace/signin.html', {'error': 'Please log in to add orders.'})
        # Fetch all sellers and items to display in the dropdowns
        suppliers = Supplier.objects.all()
        inventories = InventoryItem.objects.all()
        
        # Pass sellers and items to the context
        context = {
            'suppliers': suppliers,
            'inventories': inventories
        }
        return render(request, 'inventory/add_order.html', context)
    
    def post(self, request):
        try:
            doctor = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            messages.error(request, "Logged-in user is not associated with a doctor profile.")
            return redirect('Inventory:add_order')  # Redirect back to the form with error message
        
        # Prepare data for serialization
        data = request.POST.copy()
        data['doctor'] = doctor.id

        # Initialize the serializer with request data
        serializer = OrderSerializer(data=data)
        
        # Fetch sellers and items to display in the form if there are errors
        suppliers = Supplier.objects.all()
        inventories = InventoryItem.objects.all()
        
        if serializer.is_valid():
            order = serializer.save()
            messages.success(request, f'Order created successfully with the order ID of {order.id}')
            return redirect('Inventory:view_order')  # Redirect to view the orders
        else:
            # Pass sellers, items, and errors back to the form in case of validation errors
            context = {
                'suppliers': suppliers,
                'inventories': inventories,
                'errors': serializer.errors
            }
            messages.error(request, "There was an error adding the order.")
            return render(request, 'inventory/add_order.html', context)

class ViewOrders(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request,'marketplace/signin.html', {'error': 'Please log in to view orders.'})
        orders = OrderItem.objects.all()
        return render(request, 'inventory/view_orders.html', {'orders': orders})
    

def update_status(request):
    if request.method == "POST":
        if request.user.is_anonymous:
            return render(request,'marketplace/signin.html', {'error': 'Please log in to perform the action.'})
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        
        try:
            order = OrderItem.objects.get(id=order_id)
            order.status = status
            order.save()
            messages.success(request, f"Order status updated to '{status}' successfully.")
        except OrderItem.DoesNotExist:
            messages.error(request, "Order not found.")

        return redirect('Inventory:view_order')  # Redirect to the orders list page