# Order Management System

## Overview

The Order Management System is a Python-based command-line application developed to manage customer orders, calculate individual order totals, and track overall revenue.

The project demonstrates modular programming, input validation, JSON file handling, exception handling, and automated unit testing.

## Features

- Create customer orders.
- View all saved orders.
- Retrieve individual orders by ID.
- Calculate order totals.
- Calculate total revenue.
- Validate user inputs.
- Handle errors and invalid order data.
- Persist order information using JSON.
- Run automated unit tests.

## Technologies

- Python 3
- JSON
- Dataclasses
- unittest
- Git and GitHub

## Project Structure

```text
order-management-system/
├── data/
│   └── orders.json
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── order_service.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_order_service.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd order-management-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Run the application

```bash
python -m src.main
```

### 5. Run the tests

```bash
python -m unittest discover -s tests -v
```

## Order Calculation

Individual order total:

`Order Total = Quantity × Price Per Item`

Overall revenue:

`Total Revenue = Sum of All Order Totals`

For example, purchasing three notebooks at ₹50 each creates an order worth ₹150.

## Error Handling

The application validates customer names, product names, quantities, and prices. Invalid values raise meaningful errors rather than being accepted as valid orders.

## Storage

Order information is stored in `data/orders.json` and loaded when the application starts.

This JSON-based storage is suitable for a small learning project. A production system would generally use a database and stronger transaction handling.

## Testing

Automated tests cover order creation, order listing, order totals, overall revenue, invalid quantities, invalid prices, missing orders, and persistence.

## Future Improvements

- Integrate a database such as MySQL or PostgreSQL.
- Add customer management.
- Build a FastAPI REST API.
- Implement authentication and authorization.
- Add order updates and cancellation.
- Create a web-based dashboard.

## Author

Namah Sharma

## Project Purpose

Developed as a Python Developer Internship Day 1 task to demonstrate fundamental software development practices.


for running main.pyis :  python -m src.main 
 for running test: python -m unittest discover -s tests -v   