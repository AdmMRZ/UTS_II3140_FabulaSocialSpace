from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['order', 'name']

class Menu(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='menus')
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category.name if self.category else None,
            "category_id": self.category.id if self.category else None,
        }

class Order(models.Model):
    ORDER_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]
    order_id = models.CharField(max_length=50, unique=True)
    table_number = models.IntegerField()
    total = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "table_number": self.table_number,
            "total": self.total,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def to_dict(self):
        return {
            "menu_id": self.menu_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
        }

class TenantRequest(models.Model):
    tenant_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "tenant_name": self.tenant_name,
            "contact": self.contact,
            "type": self.type,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }
