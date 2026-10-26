from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import BaseModel, ConfigDict, Field

from src.order_service import OrderService


app = FastAPI(
    title="Order Management System API",
    description=(
        "REST API for creating orders, retrieving order details, "
        "and calculating total revenue."
    ),
    version="1.0.0",
)

class OrderCreate(BaseModel):
    customer_name: str = Field(
        min_length=1,
        max_length=100,
        description="Customer's name",
    )
    product_name: str = Field(
        min_length=1,
        max_length=150,
        description="Name of the product",
    )
    quantity: int = Field(
        gt=0,
        description="Number of items",
    )
    price: float = Field(
        gt=0,
        allow_inf_nan=False,
        description="Price per item",
    )

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    customer_name: str
    product_name: str
    quantity: int
    price: float
    total: float
    created_at: str


class RevenueResponse(BaseModel):
    total_revenue: float

@lru_cache(maxsize=1)
def get_service() -> OrderService:

    try:
        return OrderService()
    except (OSError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Order storage is unavailable: {error}",
        ) from error


@app.get("/", tags=["General"])
def home():
    return {
        "message": "Order Management System API is running.",
        "docs": "/docs",
    }


@app.get("/health", tags=["General"])
def health_check():
    return {"status": "healthy"}


@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Orders"],
)
def create_order(
    order_data: OrderCreate,
    service: OrderService = Depends(get_service),
):
    """Create and save a new order."""
    try:
        order = service.add_order(
            customer_name=order_data.customer_name.strip(),
            product_name=order_data.product_name.strip(),
            quantity=order_data.quantity,
            price=order_data.price,
        )
        return order

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the order.",
        ) from error


@app.get(
    "/orders",
    response_model=list[OrderResponse],
    tags=["Orders"],
)
def get_all_orders(
    service: OrderService = Depends(get_service),):
    try:
        return service.list_orders()

    except (OSError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve orders.",
        ) from error


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    tags=["Orders"],
)
def get_order(
    order_id: int = Path(gt=0, description="ID of the order"),
    service: OrderService = Depends(get_service),):
    try:
        return service.get_order_by_id(order_id)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve the order.",
        ) from error


@app.get(
    "/revenue",
    response_model=RevenueResponse,
    tags=["Revenue"],)
def get_total_revenue(
    service: OrderService = Depends(get_service),):
    try:
        return {
            "total_revenue": service.calculate_revenue(),
        }

    except (OSError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to calculate total revenue.",
        ) from error