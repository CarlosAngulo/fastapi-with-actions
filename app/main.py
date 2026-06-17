from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import products

app = FastAPI(
    title="Product Catalog API",
    description="A basic product catalog API built with FastAPI, ready to scale to PostgreSQL.",
    version="1.0.0"
)

# Include API Routers
app.include_router(products.router)

@app.get("/", include_in_schema=False)
def root():
    """Redirect root path to interactive API documentation."""
    return RedirectResponse(url="/docs")
