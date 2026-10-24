import tempfile
import unittest
from pathlib import Path

from src.order_service import OrderService


class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "orders.json"
        self.order_service = OrderService(
            storage_path=self.storage_path
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_order(self):
        order = self.order_service.add_order(
            customer_name="Namah",
            product_name="Smartphone Case",
            quantity=3,
            price=19.99,
        )

        self.assertEqual(order.customer_name, "Namah")
        self.assertEqual(order.product_name, "Smartphone Case")
        self.assertEqual(order.quantity, 3)
        self.assertEqual(order.price, 19.99)
        self.assertAlmostEqual(order.total, 59.97, places=2)

    def test_list_orders(self):
        self.order_service.add_order(
            customer_name="Namah",
            product_name="Smartphone Case",
            quantity=3,
            price=19.99,
        )

        orders = self.order_service.list_orders()

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].customer_name, "Namah")

    def test_individual_order_total(self):
        order = self.order_service.add_order(
            customer_name="Namah",
            product_name="Smartphone Case",
            quantity=3,
            price=19.99,
        )

        self.assertAlmostEqual(order.total, 59.97, places=2)

    def test_total_revenue(self):
        self.order_service.add_order(
            customer_name="Sumit",
            product_name="Smartphone Case",
            quantity=3,
            price=19.99,
        )
        self.order_service.add_order(
            customer_name="Vikas",
            product_name="Laptop Stand",
            quantity=2,
            price=49.99,
        )

        self.assertAlmostEqual(
            self.order_service.calculate_revenue(),
            159.95,
            places=2,
        )

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.order_service.add_order(
                customer_name="Namah",
                product_name="Smartphone Case",
                quantity=-1,
                price=19.99,
            )

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            self.order_service.add_order(
                customer_name="Namah",
                product_name="Smartphone Case",
                quantity=3,
                price=-19.99,
            )

    def test_empty_customer_name(self):
        with self.assertRaises(ValueError):
            self.order_service.add_order(
                customer_name="",
                product_name="Smartphone Case",
                quantity=3,
                price=19.99,
            )

    def test_order_persists_after_restart(self):
        self.order_service.add_order(
            customer_name="Namah",
            product_name="Smartphone Case",
            quantity=3,
            price=19.99,
        )

        restarted_service = OrderService(
            storage_path=self.storage_path
        )
        orders = restarted_service.list_orders()

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].customer_name, "Namah")


if __name__ == "__main__":
    unittest.main()