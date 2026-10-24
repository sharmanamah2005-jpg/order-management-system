import json
import math
from pathlib import Path

from src.models import Order


class OrderService:


    def __init__(self, storage_path: str = "data/orders.json"):
        self.storage_path = Path(storage_path)

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.storage_path.exists():
            self.storage_path.write_text("[]", encoding="utf-8")

        self.orders = self._load_orders()

    def _load_orders(self) -> list[Order]:
       
        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Order storage must contain a list.")

            orders = [Order.from_dict(item) for item in data]

            order_ids = [order.order_id for order in orders]

            for order_id in order_ids:
                if (
                    isinstance(order_id, bool)
                    or not isinstance(order_id, int)
                    or order_id <= 0
                ):
                    raise ValueError(
                        "Stored order IDs must be positive integers."
                    )

            if len(order_ids) != len(set(order_ids)):
                raise ValueError("Duplicate order IDs found in storage.")

            for order in orders:
                self._validate_order(
                    order.customer_name,
                    order.product_name,
                    order.quantity,
                    order.price,
                )

            return orders

        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError(
                "Order storage contains invalid data."
            ) from exc

    @staticmethod
    def _validate_order(
        customer_name: str,
        product_name: str,
        quantity: int,
        price: float,
    ) -> None:

        if not isinstance(customer_name, str) or not customer_name.strip():
            raise ValueError(
                "Customer name must be a non-empty string."
            )

        if not isinstance(product_name, str) or not product_name.strip():
            raise ValueError(
                "Product name must be a non-empty string."
            )

        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError("Price must be numeric.")
        if not math.isfinite(price):
            raise ValueError("Price must be a finite number.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

    def add_order(
        self,
        customer_name: str,
        product_name: str,
        quantity: int,
        price: float,
    ) -> Order:

        self._validate_order(
            customer_name,
            product_name,
            quantity,
            price,
        )

        order_id = max(
            (order.order_id for order in self.orders),
            default=0,
        ) + 1

        order = Order.create(
            order_id=order_id,
            customer_name=customer_name.strip(),
            product_name=product_name.strip(),
            quantity=quantity,
            price=round(float(price), 2),
        )

        self.orders.append(order)

        try:
            self.save_orders()
        except OSError:
            self.orders.pop()
            raise

        return order

    def list_orders(self) -> list[Order]:

        return self.orders.copy()

    def get_order_by_id(self, order_id: int) -> Order:
       
        if isinstance(order_id, bool) or not isinstance(order_id, int):
            raise ValueError("Order ID must be an integer.")

        if order_id <= 0:
            raise ValueError("Order ID must be positive.")

        for order in self.orders:
            if order.order_id == order_id:
                return order

        raise ValueError(f"Order with ID {order_id} not found.")

    def calculate_revenue(self) -> float:
    

        return round(
            sum(order.total for order in self.orders),
            2,
        )

    def save_orders(self) -> None:
    
        data = [order.to_dict() for order in self.orders]

        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)