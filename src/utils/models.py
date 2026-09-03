from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class ShoeCategory(str, Enum):
    HERREN = "Herren"
    DAMEN = "Damen"
    KINDER = "Kinder"
    UNISEX = "Unisex"

class ProductRecommendation(BaseModel):
    product_name: str = Field(description="Name des empfohlenen Barfußschuhs")
    price: float = Field(description="Preis in Euro")
    reason: str = Field(description="Warum dieser Schuh zum Kunden passt")
    category: ShoeCategory

class CustomerQuery(BaseModel):
    intent: Literal["recommendation", "support", "inventory_check", "research"]
    details: str

class InventoryAlert(BaseModel):
    product_name: str
    current_stock: int
    alert_level: Literal["LOW", "CRITICAL", "OK"]
