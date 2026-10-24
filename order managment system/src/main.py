from src.order_service import OrderService


def display_menu() -> None:
    print("\n===== ORDER MANAGEMENT SYSTEM =====")
    print("1. Add Order")
    print("2. View All Orders")
    print("3. View Order Total")
    print("4. View Total Revenue")
    print("5. Exit")


def add_order(service: OrderService) -> None:
    try:
        customer_name = input("Enter customer name: ").strip()
        product_name = input("Enter product name: ").strip()
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))

        order = service.add_order(
            customer_name=customer_name,
            product_name=product_name,
            quantity=quantity,
            price=price,
        )

        print("\nOrder added successfully!")
        print(f"Order ID: {order.order_id}")
        print(f"Customer: {order.customer_name}")
        print(f"Product: {order.product_name}")
        print(f"Quantity: {order.quantity}")
        print(f"Price per item: ₹{order.price:.2f}")
        print(f"Order Total: ₹{order.total:.2f}")

    except ValueError as error:
        print(f"Invalid input: {error}")

    except OSError as error:
        print(f"Unable to save the order: {error}")


def view_orders(service: OrderService) -> None:
    try:
        orders = service.list_orders()

        if not orders:
            print("\nNo orders found.")
            return

        print("\n===== ALL ORDERS =====")

        for order in orders:
            print("-" * 40)
            print(f"Order ID: {order.order_id}")
            print(f"Customer: {order.customer_name}")
            print(f"Product: {order.product_name}")
            print(f"Quantity: {order.quantity}")
            print(f"Price per item: ₹{order.price:.2f}")
            print(f"Total: ₹{order.total:.2f}")
            print(f"Created At: {order.created_at}")

        print("-" * 40)

    except (OSError, ValueError) as error:
        print(f"Unable to retrieve orders: {error}")


def view_order_total(service: OrderService) -> None:
    try:
        order_id = int(input("Enter order ID: "))
        order = service.get_order_by_id(order_id)

        print(f"\nOrder ID: {order.order_id}")
        print(f"Customer: {order.customer_name}")
        print(f"Product: {order.product_name}")
        print(f"Quantity: {order.quantity}")
        print(f"Total: ₹{order.total:.2f}")

    except ValueError as error:
        print(f"Invalid order ID or input: {error}")

    except OSError as error:
        print(f"Unable to retrieve the order: {error}")


def view_total_revenue(service: OrderService) -> None:
    
    try:
        revenue = service.calculate_revenue()
        print(f"\nTotal Revenue: ₹{revenue:.2f}")

    except (OSError, ValueError) as error:
        print(f"Unable to calculate revenue: {error}")


def main() -> None:
    
    try:
        service = OrderService()

    except (OSError, ValueError) as error:
        print(f"Unable to initialize the order system: {error}")
        return

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_order(service)

        elif choice == "2":
            view_orders(service)

        elif choice == "3":
            view_order_total(service)

        elif choice == "4":
            view_total_revenue(service)

        elif choice == "5":
            print("Exiting Order Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    main()