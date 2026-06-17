from typing import Dict, List, Optional
import uuid

# In-memory database simulation
# This simulates a database table for products
PRODUCTS_DB: Dict[str, dict] = {
    "TSHIRT-DEP-01": {
        "id": "79164bcb-d23c-4c36-ab42-e9724c5508aa",
        "name": "Camiseta Deportiva Run",
        "sku": "TSHIRT-DEP-01",
        "price": 29.99,
        "description": "Camiseta deportiva ligera y transpirable ideal para running.",
        "photos": ["https://example.com/photos/tshirt-run-front.jpg", "https://example.com/photos/tshirt-run-back.jpg"],
        "category": "Ropa",
        "sizes": ["S", "M", "L", "XL"]
    },
    "SHOES-RUN-02": {
        "id": "8b234fae-3c58-4d57-9db6-b25862e3d368",
        "name": "Zapatillas Running Trail",
        "sku": "SHOES-RUN-02",
        "price": 89.90,
        "description": "Zapatillas con alta amortiguación y suela con agarre para senderos.",
        "photos": ["https://example.com/photos/shoes-trail-side.jpg"],
        "category": "Calzado",
        "sizes": ["40", "41", "42", "43", "44"]
    },
    "CAP-SPORT-03": {
        "id": "31fe219c-cb23-455b-a81d-e59fa2e411b0",
        "name": "Gorra Deportiva Ajustable",
        "sku": "CAP-SPORT-03",
        "price": 19.95,
        "description": "Gorra clásica deportiva con protección UV y banda absorbente.",
        "photos": ["https://example.com/photos/cap-front.jpg"],
        "category": "Accesorios",
        "sizes": ["Única"]
    }
}

def get_all_products() -> List[dict]:
    """Retrieve all products from the mock database."""
    return list(PRODUCTS_DB.values())

def get_product_by_sku(sku: str) -> Optional[dict]:
    """Retrieve a single product by its unique SKU."""
    return PRODUCTS_DB.get(sku.upper())

def create_product(product_data: dict) -> dict:
    """
    Create a new product in the mock database.
    Assigns a unique auto-generated id.
    """
    # Normalize SKU to uppercase for consistency
    sku = product_data["sku"].upper()
    
    # Store the database record
    new_product = {
        "id": str(uuid.uuid4()),
        **product_data,
        "sku": sku
    }
    PRODUCTS_DB[sku] = new_product
    return new_product

def update_product(sku: str, update_data: dict) -> Optional[dict]:
    """
    Update specific fields of an existing product.
    Only updates fields that are provided (PATCH behavior).
    """
    sku_upper = sku.upper()
    if sku_upper not in PRODUCTS_DB:
        return None
    
    current_product = PRODUCTS_DB[sku_upper]
    
    # Apply updates for provided fields
    for key, value in update_data.items():
        if value is not None:
            current_product[key] = value
            
    # If the SKU itself was changed in the update (normally SKU shouldn't change, but if it did):
    if "sku" in update_data and update_data["sku"]:
        new_sku = update_data["sku"].upper()
        if new_sku != sku_upper:
            current_product["sku"] = new_sku
            PRODUCTS_DB[new_sku] = current_product
            del PRODUCTS_DB[sku_upper]
            
    return current_product
