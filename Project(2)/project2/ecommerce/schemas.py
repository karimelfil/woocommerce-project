from pydantic import BaseModel, Field , EmailStr
from datetime import datetime, time
from typing import List, Optional
from ninja import Schema

class ActivityIn(BaseModel):
    date_created: datetime
    date_modified: datetime
    time_created: time

class ActivityOut(BaseModel):
    date_created: datetime
    date_modified: datetime
    time_created: time

class ItemCategoryIn(BaseModel):
    name: str
    image: str
    path : str
    parent :Optional[int] = None
    woocommerce_id :int

class ItemCategoryOut(BaseModel):
    name: str
    image: str
    path : str
    parent :Optional[int] = None
    woocommerce_id :int
   
class ItemFamilyIn(BaseModel):
    name: str
    woocommerce_id :int

class ItemFamilyOut(BaseModel):
    name: str
    woocommerce_id :int

class ItemBrandIn(BaseModel):
    name: str
    woocommerce_id :int

class ItemBrandOut(BaseModel):
    name: str
    woocommerce_id :int

class SpecsIn(BaseModel):
    description: str
    woocommerce_id :int

class SpecsOut(BaseModel):
    description: str
    woocommerce_id :int

class UnitOfMeasurementIn(BaseModel):
    name: str
    code: str
    type: List[str]
    woocommerce_id :int

class UnitOfMeasurementOut(BaseModel):
    name: str
    code: str
    type: List[str]
    woocommerce_id :int

class TagsIn(BaseModel):
    name: str
    woocommerce_id :int

class TagsOut(BaseModel):
    name: str
    woocommerce_id :int

class PackageIn(BaseModel):
    name: str
    weight: float
    length: float
    height: float
    width: float
    material: str

class PackageOut(BaseModel):
    name: str
    weight: float
    length: float
    height: float
    width: float
    materail: str

class VariationsHeaderIn(BaseModel):
    attribute: str
    woocommerce_id :int

class VariationsHeaderOut(BaseModel):
    attribute: str
    woocommerce_id :int

class VariationsDetailIn(BaseModel):
    variation_id: int  
    value: str
    woocommerce_id :int

class VariationsDetailOut(BaseModel):
    variation_id: int  
    value: str
    woocommerce_id :int

class ItemIn(BaseModel):
    name: str
    active: bool
    status : str ='published'
    description: str = ''
    role: str = 'standalone'
    sku_code: str = ''
    barcode_type: str = ''
    barcode: str = ''
    type: str = 'product'
    usage: Optional[str] = None
    unit_of_measure: List[int] = []
    tags: List[int] = []
    family_id: Optional[int] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    specs_id: List[int] = []
    is_variant: bool = False
    tracking_stock_by_variant: bool = False
    variations: List[int] = []
    selected_variations: List[int] = []
    alternative_items: List[int] = []
    returnable_item: bool = False
    width: Optional[float] = None
    width_unit_of_measure: Optional[int] = None
    height: Optional[float] = None
    height_unit_of_measure: Optional[int] = None
    length: Optional[float] = None
    length_unit_of_measure: Optional[int] = None
    weight: Optional[float] = None
    weight_unit_of_measure: Optional[int] = None
    available_in_pos: bool = False
    shelf_life: Optional[str] = ''
    end_of_life: Optional[str] = ''
    allow_sales: bool = True
    max_discount_sales: Optional[float] = None
    default_sale_unit_of_measure: Optional[int] = None
    default_selling_price: Optional[float] = None
    default_selling_price_usd: Optional[float] = None
    default_cost: Optional[float] = None
    default_cost_usd: Optional[float] = None
    lead_time: Optional[str] = ''
    minimum_quantity_order: Optional[float] = None
    default_purchase_unit_of_measure: Optional[int] = None
    minimum_quantity_in_stock: Optional[float] = None
    warranty_period: Optional[str] = ''
    allow_negative_stock: bool = False
    auto_reorder: bool = False
    variant_of: Optional[int] = None
    price: float = 0.0
    regular_price: float = 0.0
    sales_price: float = 0.0
    woocommerce_id :int

class ItemCreate(BaseModel):
    name: str
    active: bool
    status : str ='published'
    description: str = ''
    role: str = 'standalone'
    sku_code: str = ''
    barcode_type: str = ''
    barcode: str = ''
    type: str = 'product'
    usage: Optional[str] = None
    unit_of_measure: List[int] = []
    tags: List[int] = []
    family_id: Optional[int] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    specs_id: List[int] = []
    is_variant: bool = False
    tracking_stock_by_variant: bool = False
    variations: List[int] = []
    selected_variations: List[int] = []
    alternative_items: List[int] = []
    returnable_item: bool = False
    width: Optional[float] = None
    width_unit_of_measure: Optional[int] = None
    height: Optional[float] = None
    height_unit_of_measure: Optional[int] = None
    length: Optional[float] = None
    length_unit_of_measure: Optional[int] = None
    weight: Optional[float] = None
    weight_unit_of_measure: Optional[int] = None
    available_in_pos: bool = False
    shelf_life: Optional[str] = ''
    end_of_life: Optional[str] = ''
    allow_sales: bool = True
    max_discount_sales: Optional[float] = None
    default_sale_unit_of_measure: Optional[int] = None
    default_selling_price: Optional[float] = None
    default_selling_price_usd: Optional[float] = None
    default_cost: Optional[float] = None
    default_cost_usd: Optional[float] = None
    lead_time: Optional[str] = ''
    minimum_quantity_order: Optional[float] = None
    default_purchase_unit_of_measure: Optional[int] = None
    minimum_quantity_in_stock: Optional[float] = None
    warranty_period: Optional[str] = ''
    allow_negative_stock: bool = False
    auto_reorder: bool = False
    variant_of: Optional[int] = None
    price: float = 0.0
    regular_price: float = 0.0
    sales_price: float = 0.0
    woocommerce_id :int

class ItemPackageIn(BaseModel):
    item_id: int  
    package_id: int  
    quantity: float
    barcode: str

class ItemPackageOut(BaseModel):
    item_id: int  
    package_id: int  
    quantity: float
    barcode: str

class ItemsWarehouseIn(BaseModel):
    warehouse_id: int
    item_id: int  
    quantity: float
    net_movement: float
    quantity_reserved: float
    branch: int
    opening: bool
    opening_quantity: int

class ItemsWarehouseOut(BaseModel):
    warehouse_id: int
    item_id: int  
    quantity: float
    net_movement: float
    quantity_reserved: float
    branch: int
    opening: bool
    opening_quantity: int

class WarehouseIn(BaseModel):
    name: str
    country: str
    city: str
    address: str
    branch: int
    initial_data: bool
    default: bool
    show_room: bool

class WarehouseOut(WarehouseIn):
    id: int

class IntegrateIn(BaseModel):
    type: str
    consumer_key: str
    secret_key: str
    active: bool
    warehouse: WarehouseIn

class IntegrateOut(IntegrateIn):
    id: int

class IntegrateOutt(IntegrateIn):
    id: int
    warehouse: Optional[WarehouseOut] = None

class ItemOut(BaseModel):
    name: str
    active: bool
    description: str
    role: str
    sku_code: str
    barcode_type: str
    barcode: str
    type: str
    usage: Optional[str]
    unit_of_measure: List[int] = []
    tags: List[int] = []
    family_id: Optional[int]
    brand_id: Optional[int]
    category_id: Optional[int]
    specs_id: List[int] = []
    is_variant: bool
    tracking_stock_by_variant: bool
    variations: List[int] = []
    selected_variations: List[int] = []
    alternative_items: List[int] = []
    returnable_item: bool
    width: Optional[float]
    width_unit_of_measure: Optional[int]
    height: Optional[float]
    height_unit_of_measure: Optional[int]
    length: Optional[float]
    length_unit_of_measure: Optional[int]
    weight: Optional[float]
    weight_unit_of_measure: Optional[int]
    available_in_pos: bool
    shelf_life: Optional[str]
    end_of_life: Optional[str]
    allow_sales: bool
    max_discount_sales: Optional[float]
    default_sale_unit_of_measure: Optional[int]
    default_selling_price: Optional[float]
    default_selling_price_usd: Optional[float]
    default_cost: Optional[float]
    default_cost_usd: Optional[float]
    lead_time: Optional[str]
    minimum_quantity_order: Optional[float]
    default_purchase_unit_of_measure: Optional[int]
    minimum_quantity_in_stock: Optional[float]
    warranty_period: Optional[str]
    allow_negative_stock: bool
    auto_reorder: bool
    variant_of: Optional[int]
    price: float
    regular_price: float
    sales_price: float
    woocommerce_id :int

    class Config:
        from_attributes = True  

class SuccessResponse(Schema):
    success: bool
    message: str

class ErrorResponse(Schema):
    error: str

class PriceUpdateSchema(Schema):
    new_price: float