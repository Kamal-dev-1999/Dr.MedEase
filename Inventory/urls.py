from django.urls import path
from .views import AddInventoryView , AddSellerView , ViewInventory ,AddOrderView , ViewOrders , update_status

app_name = 'Inventory'

urlpatterns = [
    path('add_inventory/', AddInventoryView.as_view(), name='add_inventory'),
    path('add_seller/', AddSellerView.as_view(), name='add_seller'),
    path('view_inventory/',ViewInventory.as_view(),name='view_inventory'),
    path('add_order/',AddOrderView.as_view(),name='add_order'),
    path('view_orders/',ViewOrders.as_view(),name='view_order'),
    path('updated_status/',update_status,name='update_status')
]
