import requests
from django.conf import settings
from .repositories import MenuRepository, OrderRepository, TenantRepository
from .models import Menu
import uuid

GOOGLE_TOKENINFO = "https://oauth2.googleapis.com/tokeninfo"

class AuthService:
    @staticmethod
    def verify_google_token(credential):
        r = requests.get(GOOGLE_TOKENINFO, params={"id_token": credential}, timeout=5)
        if r.status_code != 200:
            return None
        payload = r.json()
        
        return {
            "name": payload.get("name"),
            "email": payload.get("email"),
            "picture": payload.get("picture"),
            "token": credential
        }

class MenuService:
    @staticmethod
    def list_menus():
        menus = MenuRepository.list_all()
        return [m.to_dict() for m in menus]

    @staticmethod
    def create_menu(name, description="", price=None, image_url="", category=None):
        if not name:
            raise ValueError("name is required")
        
        m = MenuRepository.create(
            name=name, 
            description=description, 
            price=price, 
            image_url=image_url,
            category=category
        )
        return m.to_dict()

class OrderService:
    @staticmethod
    def _generate_order_id():
        return f"ORD-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    def create_order(table_number, items):
        items_data = []
        total = 0
        for it in items:
            menu = MenuRepository.get_by_id(it["menu_id"])
            if not menu:
                raise ValueError(f"menu_id {it['menu_id']} not found")
            qty = int(it.get("quantity", 1))
            price = menu.price
            subtotal = price * qty
            total += subtotal
            items_data.append({
                "menu_id": menu.id,
                "name": menu.name,
                "quantity": qty,
                "price": price
            })
        order_id = OrderService._generate_order_id()
        order = OrderRepository.create_order(order_id, table_number, items_data, total)

        return {
            "order_id": order.order_id,
            "total": total,
            "status": "pending"
        }

    @staticmethod
    def confirm_payment(order_id):
        order = OrderRepository.update_order_status(order_id, "paid")
        if not order:
            raise ValueError(f"Order {order_id} not found")
        return order.to_dict()

class TenantService:
    @staticmethod
    def create_tenant_request(tenant_name, contact, type_, description):
        tr = TenantRepository.create_request(tenant_name, contact, type_, description)
        return tr.to_dict()