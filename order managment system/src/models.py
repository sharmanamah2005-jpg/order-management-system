from dataclasses import dataclass
from datetime import datetime
import math


@dataclass
class Order:

    order_id: int
    customer_name: str
    product_name: str
    quantity: int
    price: float
    created_at: str

    @property
    def total(self) -> float:
        return round(self.quantity * self.price, 2)

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.total,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        if not isinstance(data, dict):
            raise ValueError("Each stored order must be a dictionary.")

        try:
            order = cls(
                order_id=int(data["order_id"]),
                customer_name=data["customer_name"],
                product_name=data["product_name"],
                quantity=int(data["quantity"]),
                price=float(data["price"]),
                created_at=data["created_at"],
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Stored order contains missing or invalid fields.") from error

        if isinstance(data["order_id"], bool) or order.order_id <= 0:
            raise ValueError("Order ID must be a positive integer.")

        if not isinstance(order.customer_name, str) or not order.customer_name.strip():
            raise ValueError("Customer name cannot be empty.")

        if not isinstance(order.product_name, str) or not order.product_name.strip():
            raise ValueError("Product name cannot be empty.")

        if isinstance(data["quantity"], bool) or order.quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if not math.isfinite(order.price) or order.price <= 0:
            raise ValueError("Price must be a finite positive number.")

        if not isinstance(order.created_at, str) or not order.created_at.strip():
            raise ValueError("Order creation date is missing.")

        return order

    @classmethod
    def create(
        cls,
        order_id: int,
        customer_name: str,
        product_name: str,
        quantity: int,
        price: float,
    ) -> "Order":
        return cls(
            order_id=order_id,
            customer_name=customer_name,
            product_name=product_name,
            quantity=quantity,
            price=round(float(price), 2),
            created_at=datetime.now().isoformat(timespec="seconds"),
        )