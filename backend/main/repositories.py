from .models import Menu, Order, OrderItem, TenantRequest
from django.db import transaction
from django.utils import timezone

class MenuRepository:
    @staticmethod
    def list_all():
        return list(Menu.objects.all())

    @staticmethod
    def get_by_id(menu_id):
        return Menu.objects.filter(id=menu_id).first()

    @staticmethod
    def create(name, description="", price=None, image_url="", category=None):
        from .models import Category
        
        if category:
            cat, _ = Category.objects.get_or_create(name=category)
        else:
            cat = None
            
        m = Menu.objects.create(
            name=name,
            description=description or "",
            price=price,
            image_url=image_url or "",
            category=cat
        )
        return m

class OrderRepository:
    @staticmethod
    @transaction.atomic
    def create_order(order_id, table_number, items_data, total):
        order = Order.objects.create(order_id=order_id, table_number=table_number, total=total, status="paid")
        for it in items_data:
            OrderItem.objects.create(
                order=order,
                menu_id=it["menu_id"],
                name=it["name"],
                quantity=it["quantity"],
                price=it["price"],
            )
        return order

class TenantRepository:
    @staticmethod
    def create_request(tenant_name, contact, type_, description):
        return TenantRequest.objects.create(
            tenant_name=tenant_name,
            contact=contact,
            type=type_,
            description=description
        )