from typing import List, Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the product")
    sku: str = Field(..., min_length=3, max_length=50, description="Unique Stock Keeping Unit code")
    price: float = Field(..., gt=0.0, description="Price of the product, must be greater than zero")
    description: Optional[str] = Field(None, max_length=1000, description="Optional detailed description of the product")
    photos: List[str] = Field(default=[], description="List of photo URLs for the product")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    sizes: List[str] = Field(default=[], description="List of available sizes (e.g., S, M, L, XL or numeric values)")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sku: Optional[str] = Field(None, min_length=3, max_length=50)
    price: Optional[float] = Field(None, gt=0.0)
    description: Optional[str] = Field(None, max_length=1000)
    photos: Optional[List[str]] = Field(None)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    sizes: Optional[List[str]] = Field(None)

class ProductResponse(ProductBase):
    id: str = Field(..., description="Unique database identifier")

    class Config:
        # Pydantic v2 configuration (allows serialization from dict or class attributes)
        from_attributes = True
