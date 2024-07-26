from rest_framework import status
from .models import *
from .views import create_woocommerce_category  
from unittest.mock import patch , MagicMock
from .urls import *
from django.test import TestCase, RequestFactory
from .schemas import*
from django.urls import *
from decimal import Decimal


#Category tester :

# class ItemCategoryTests(TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()

#     @patch('ecommerce.views.create_woocommerce_category')
#     def test_create_category(self, mock_create_woocommerce_category):
#         mock_create_woocommerce_category.return_value = 123  

#         data = {
#             "name": "Electronics",
#             "image": "http://example.com/image.jpg",  
#             "path": "/electronics/",
#             "parent": None,
#             "woocommerce_id": None  
#         }

#         request = self.factory.post('/category/', json.dumps(data), content_type='application/json')
#         payload = ItemCategoryIn(**data)  
#         response = create_category(request, payload=payload)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(ItemCategory.objects.count(), 1)
#         category = ItemCategory.objects.get()
#         self.assertEqual(category.name, 'Electronics')
#         self.assertEqual(category.woocommerce_id, 123)
#         self.assertIsNone(category.parentt)

#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['name'], 'Electronics')
#         self.assertEqual(response_data['path'], '/electronics/')
#         self.assertEqual(response_data['woocommerce_id'], 123)
#         self.assertIsNone(response_data['parent'])


# #Family Tester :

# class FamilyTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
    
#     @patch('ecommerce.views.create_woocommerce_attrubites')
#     def test_create_family(self, mock_create_woocommerce_attributes):
#         mock_create_woocommerce_attributes.return_value = 123

#         data = {
#             "name": "electronics",
#         }

#         request = self.factory.post('/family/', json.dumps(data), content_type='application/json')
#         payload = ItemFamilyIn(**data)
#         response = create_family(request, payload=payload)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(ItemFamily.objects.count(), 1)
#         family = ItemFamily.objects.get()
#         self.assertEqual(family.name, 'electronics')

#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['name'], 'electronics')

# #Specs Tester:

# class SpecsTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#     @patch('ecommerce.views.create_woocommerce_attrubites')
#     def test_create_specs(self, mock_create_woocommerce_attributes):
#         mock_create_woocommerce_attributes.return_value = 123

#         data = {
#             "description": "high quality",
#         }

#         request = self.factory.post('/specs/', json.dumps(data), content_type='application/json')
#         payload = SpecsIn(**data)
#         response = create_specs(request, payload=payload)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Specs.objects.count(), 1)
#         specs = Specs.objects.get()
#         self.assertEqual(specs.description, "high quality")
#         self.assertEqual(specs.woocommerce_id, 123)


#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['description'], "high quality")
#         self.assertEqual(response_data['woo_id'], 123)

# #Unitmeasure Tester :

# class UnitmeasureTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#     @patch('ecommerce.views.create_woocommerce_attrubites')
#     def test_create_unitmeasure(self, mock_create_woocommerce_attributes):
#         mock_create_woocommerce_attributes.return_value = 123
#         data = {
#             "name": "cm",
#             "type": ["pppp"],
#             'code' : "a45a",
#             "woocommerce_id": None  

#         }

#         request = self.factory.post('/unitmeasurments/', json.dumps(data), content_type='application/json')
#         payload = UnitOfMeasurementIn(**data)
#         response = create_unitmeasurments(request, payload=payload)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(UnitOfMeasurment.objects.count(), 1)
#         unitOfMeasurment = UnitOfMeasurment.objects.get()
#         self.assertEqual(unitOfMeasurment.name, "cm")
#         self.assertEqual(unitOfMeasurment.woocommerce_id, 123)
#         self.assertEqual(unitOfMeasurment.type, ["pppp"])
#         self.assertEqual(unitOfMeasurment.code, "a45a")

#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['name'], "cm")
#         self.assertEqual(response_data['type'], ["pppp"])
#         self.assertEqual(response_data['code'], "a45a")

# #Tags Tester :

# # class TagsTests(TestCase):
# #     def setUp(self):
# #         self.factory = RequestFactory()
# #     @patch('ecommerce.views.create_woocommerce_tags')
# #     def test_create_tags(self, mock_create_woocommerce_tags):
# #         mock_create_woocommerce_tags.return_value = 41 
# #         data = {
# #             "name": "bye",
# #             "woocommerce_id": None 
# #         }

# #         request = self.factory.post('/tags/', json.dumps(data), content_type='application/json')
# #         payload = TagsIn(**data)
# #         response = create_tags(request, payload=payload)

# #         self.assertEqual(response.status_code, 200)
# #         self.assertEqual(Tags.objects.count(), 1)
# #         tags = Tags.objects.get()
# #         self.assertEqual(tags.name, "bye")
# #         self.assertEqual(tags.woocommerce_id, 41) 
# #         response_data = json.loads(response.content)
# #         self.assertEqual(response_data['name'], "bye")
# #         self.assertEqual(response_data['woocommerce_id'], 41)


# #Variation header Tester :

# class VariationHeaderTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#     @patch('ecommerce.views.create_woocommerce_attrubites')
#     def test_create_header(self, mock_create_woocommerce_attributes):
#         mock_create_woocommerce_attributes.return_value = 123

#         data = {
#             "attribute": "hjhjjjj",
#             "woocommerce_id": None             
#         }

#         request = self.factory.post('/header/', json.dumps(data), content_type='application/json')
#         payload = VariationsHeaderIn(**data)
#         response = create_VariationsHeader(request, payload=payload)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(VariationsHeader.objects.count(), 1)
#         header = VariationsHeader.objects.get()
#         self.assertEqual(header.attribute, 'hjhjjjj')
#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['attribute'], 'hjhjjjj')

# # #Item Tester:

# class CreateItemTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         self.tag = Tags.objects.create(name="Tag 1")
#         self.family = ItemFamily.objects.create(name="Family 1")
#         self.brand = ItemBrand.objects.create(name="Brand 1")
#         self.spec = Specs.objects.create(description="Spec 1")

#     def test_create_item(self):
#         url = '/api/items/' 
#         data = {
#             "name": "Test Item",
#             "active": True,
#             "status": "published",
#             "description": "This is a test item.",
#             "role": "standalone",
#             "sku_code": "SKU123",
#             "barcode_type": "EAN",
#             "barcode": "1234567890123",
#             "type": "product",
#             "usage": None,
#             "is_variant": False,
#             "tracking_stock_by_variant": False,
#             "returnable_item": False,
#             "width": 10.0,
#             "height": 20.0,
#             "length": 30.0,
#             "weight": 5.0,
#             "available_in_pos": False,
#             "shelf_life": "",
#             "end_of_life": "",
#             "allow_sales": True,
#             "max_discount_sales": 10.0,
#             "default_selling_price": 100.0,
#             "default_selling_price_usd": 120.0,
#             "default_cost": 80.0,
#             "default_cost_usd": 96.0,
#             "lead_time": "",
#             "minimum_quantity_order": 1.0,
#             "minimum_quantity_in_stock": 2.0,
#             "warranty_period": "",
#             "allow_negative_stock": False,
#             "auto_reorder": False,
#             "variant_of": None,
#             "price": 100.0,
#             "regular_price": 120.0,
#             "sales_price": 90.0,
#             "woocommerce_id": 3077,
#             "tags": [self.tag.id],
#             "family_id": self.family.id,
#             "brand_id": self.brand.id,
#             "specs_id": [self.spec.id],
#             "alternative_items": []
#         }

#         response = self.client.post(url, data, format='json')


#         response_data = response.json()


#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_data['success'], True)

#         self.assertTrue(Item.objects.filter(name="Test Item").exists())
#         item = Item.objects.get(name="Test Item")
#         self.assertEqual(item.woocommerce_id, 3077)
#         self.assertEqual(item.tags.count(), 1)
#         self.assertEqual(item.tags.first().id, self.tag.id)
#         self.assertEqual(item.family.id, self.family.id)
#         self.assertEqual(item.brand.id, self.brand.id)
#         self.assertEqual(item.specs.count(), 1)
#         self.assertEqual(item.specs.first().id, self.spec.id)
#         self.assertEqual(item.default_selling_price, Decimal('100.00'))
#         self.assertEqual(item.default_selling_price_usd, Decimal('120.00'))
#         self.assertEqual(item.default_cost, Decimal('80.00'))
#         self.assertEqual(item.default_cost_usd, Decimal('96.00'))
#         self.assertEqual(item.price, Decimal('100.00'))
#         self.assertEqual(item.regular_price, Decimal('120.00'))
#         self.assertEqual(item.sales_price, Decimal('90.00'))

#Customer :

# class CustomerCreateTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_create_customer_success(self):

#         billing_address = BillingAddress.objects.create(
#             first_name="John",
#             last_name="Doe",
#             address_1="123 Main St",
#             city="Anytown",
#             state="CA",
#             country="US",
#             postcode="12345",
#             phone="741",
#             email="lkjhgfd@gmail.com",
#             company="jhgfd"
#         )

#         shipping_address = ShippingAddress.objects.create(
#             first_name="John",
#             last_name="Doe",
#             address_1="123 Main St",
#             city="Anytown",
#             state="CA",
#             country="US",
#             postcode="12345",
#             company="jhgfd"
#         )

#         data = {
#             "email": "test@example.com",
#             "first_name": "John",
#             "last_name": "Doe",
#             "role": "customer",
#             "username": "johndoe",
#             "password": "password",
#             "is_paying_customer": True,
#             "avatar_url": "https://example.com/avatar.jpg",
#             "customerbiling_id": billing_address.id,
#             "customershipping_id": shipping_address.id,
#             "woocommerce_id": 123  
#         }

#         request = self.factory.post('/customers/', json.dumps(data), content_type='application/json')
#         response = create_customer(request, payload=CustomerIn(**data))


#         self.assertEqual(response.status_code, 201) 


#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['email'], "test@example.com")
#         self.assertEqual(response_data['first_name'], "John")
#         self.assertEqual(response_data['last_name'], "Doe")


#         self.assertEqual(Customer.objects.count(), 1)
#         customer = Customer.objects.get(email="test@example.com")
#         self.assertEqual(customer.username, "johndoe")
#         self.assertEqual(customer.role, "customer")


# #Order Tester:

# class OrderCreateTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_create_order_success(self):

#         billing_address = BillingAddress.objects.create(
#             first_name="John",
#             last_name="Doe",
#             address_1="123 Main St",
#             city="Anytown",
#             state="CA",
#             country="US",
#             postcode="12345",
#             phone="741",
#             email="billing@example.com",
#             company="Billing Company"
#         )

#         shipping_address = ShippingAddress.objects.create(
#             first_name="Jane",
#             last_name="Smith",
#             address_1="456 Elm St",
#             city="Anytown",
#             state="CA",
#             country="US",
#             postcode="54321",
#             company="Shipping Company"
#         )

#         customer = Customer.objects.create(
#             email="customer@example.com",
#             first_name="John",
#             last_name="Doe",
#             role="customer",
#             username="johndoe",
#             password="password",
#             is_paying_customer=True,
#             avatar_url="https://example.com/avatar.jpg",
#             customerbiling_id=billing_address,
#             customershipping_id=shipping_address
#         )

#         data = {
#             "parent_id": None,  
#             "number": "12345",  
#             "order_key": "abcdefg12345",  
#             "created_via": "API", 
#             "version": "1.0",  
#             "status": "processing", 
#             "currency": "USD", 
#             "discount_total": 0.0,
#             "discount_tax": 0.0,
#             "shipping_total": 5.0,
#             "shipping_tax": 0.5,
#             "cart_tax": 1.0,
#             "total": 50.0,
#             "total_tax": 5.5,
#             "prices_include_tax": False,
#             "payment_method": "credit_card",  
#             "date_paid": None, 
#             "date_completed": None,  
#             "cart_hash": "abc123",  
#             "set_paid": False,
#             "woocommerce_id": 123,  
#             "customer_id": customer.id,
#             "customerbiling_id": billing_address.id,
#             "customershipping_id": shipping_address.id
#         }

#         request = self.factory.post('/orders/', json.dumps(data), content_type='application/json')
#         response = create_order(request, payload=OrderIn(**data))


#         self.assertEqual(response.status_code, 201)  


#         response_data = json.loads(response.content)
#         self.assertEqual(response_data['number'], "12345")
#         self.assertEqual(response_data['status'], "processing")


#         self.assertEqual(Order.objects.count(), 1)
#         order = Order.objects.get(number="12345")  
#         self.assertEqual(order.payment_method, "credit_card")
#         self.assertEqual(order.total, 50.0)