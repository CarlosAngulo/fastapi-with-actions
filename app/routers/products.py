from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app import database

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(product_in: ProductCreate):
    """
    Create a new product.
    Checks if a product with the same SKU already exists.
    """
    sku_upper = product_in.sku.upper()
    existing_product = database.get_product_by_sku(sku_upper)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product_in.sku}' already exists."
        )
    
    # Store product
    new_product = database.create_product(product_in.model_dump())
    return new_product

@router.get("/", response_model=List[ProductResponse])
def read_all_products():
    """
    Retrieve all products.
    """
    return database.get_all_products()

@router.get("/{sku}", response_model=ProductResponse)
def read_product_by_sku(sku: str):
    """
    Retrieve a specific product by SKU.
    """
    product = database.get_product_by_sku(sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU '{sku}' not found."
        )
    return product

@router.patch("/{sku}", response_model=ProductResponse)
def update_existing_product(sku: str, product_in: ProductUpdate):
    """
    Update field values of an existing product (PATCH).
    If a new SKU is provided, it checks if it conflicts with another product.
    """
    sku_upper = sku.upper()
    product = database.get_product_by_sku(sku_upper)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU '{sku}' not found."
        )
    
    # Extract data provided in request body, ignoring unset/None values
    update_data = product_in.model_dump(exclude_unset=True)
    if not update_data:
        # No updates provided, return product as is
        return product
    
    # If the SKU is being changed, verify the new one is not already taken
    if "sku" in update_data:
        new_sku = update_data["sku"].upper()
        if new_sku != sku_upper:
            conflict = database.get_product_by_sku(new_sku)
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot change SKU to '{update_data['sku']}' because it is already in use by another product."
                )
                
    updated_product = database.update_product(sku, update_data)
    return updated_product
