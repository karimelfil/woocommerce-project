from django.shortcuts import get_object_or_404
from ecommerce.models import *
from ninja import NinjaAPI , Path
from .schemas import *
from django.http import  JsonResponse  , HttpResponse 
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ninja.errors import HttpError
import requests
from django.db import transaction
from django.db import IntegrityError
api = NinjaAPI()
from requests.auth import HTTPBasicAuth

#WOOCOMMERCE INTEGRATION : 
from django.conf import settings
def create_woocommerce_category(name, slug):
    url = 'https://eldrapaints.com/wp-json/wc/v3/products/categories'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'name': name,
        'slug': slug
    }

    response = requests.post(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print('Failed to create category')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None
    
def create_woocommerce_tags(name, slug):
    url = 'https://eldrapaints.com/wp-json/wc/v3/products/tags'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'name': name,
        'slug': slug
    }

    response = requests.post(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print('Failed to create tags')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None
    
def sync_tags():
    tags = Tags.objects.all()

    for tag in tags:
        woocommerce_tag_id = create_woocommerce_tags(tag.name, tag.name.lower().replace(' ', '-'))
        if woocommerce_tag_id:
            tag.woocommerce_id=woocommerce_tag_id
            tag.save()
            print(f"Woocommerce Tag created:'{tag.name}' with ID {woocommerce_tag_id}")
        else:
            print(f"Failed to create WooCommerce tag for  '{tag.name}' ")

def update_woocommerce_tag(tag_id, name):
    url = f'https://eldrapaints.com/wp-json/wc/v3/products/tags/{tag_id}'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'name': name,
    }

    response = requests.put(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    response.raise_for_status() 
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to update tag')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None



def update_woocommerce_category(category_id, name, path):
    url = f'https://eldrapaints.com/wp-json/wc/v3/products/categories/{category_id}'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'name': name,
        'path': path
    }

    response = requests.put(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    response.raise_for_status() 
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to update category')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None

def delete_woocommerce_category(woocommerce_id):
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    url = f'https://eldrapaints.com/wp-json/wc/v3/products/categories/{woocommerce_id}'

    response = requests.delete(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    logging.debug(f"Request URL: {response.url}")
    logging.debug(f"Request Headers: {response.request.headers}")
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Headers: {response.headers}")
    logging.debug(f"Response Content: {response.content}")

    if response.status_code in [200, 201, 204]:
        return True, None
    else:
        try:
            error_message = response.json().get('message', 'Failed to delete WooCommerce category')
        except ValueError:
            error_message = 'Response content is not valid JSON'
        
        logging.error(f"Error deleting category in WooCommerce: {error_message}")
        return False, error_message


def delete_django_category(category_id):
    try:
        category = get_object_or_404(ItemCategory, id=category_id)
        category.delete()
        return True, None
    except Exception as e:
        logging.error(f"Error deleting category in Django: {str(e)}")
        return False, str(e)

def sync_categories():
    categories = ItemCategory.objects.all()

    for category in categories:
        woocommerce_category_id = create_woocommerce_category(category.name, category.name.lower().replace(' ', '-'))
        if woocommerce_category_id:
            category.woocommerce_id = woocommerce_category_id
            category.save()
            print(f"Created WooCommerce category '{category.name}' with ID {woocommerce_category_id}")
        else:
            print(f"Failed to create WooCommerce category for '{category.name}'")

def sync_categories_update():
    categories = ItemCategory.objects.all()

    for category in categories:
        woocommerce_category_id, slug = create_woocommerce_category(category.name, category.name.lower().replace(' ', '-'))
        
        if woocommerce_category_id:
            print(f"Created WooCommerce category '{category.name}' with ID {woocommerce_category_id}")
            

            update_response = update_woocommerce_category(woocommerce_category_id, category.name, slug)
            if update_response:
                print(f"Updated WooCommerce category '{category.name}'")
            else:
                print(f"Failed to update WooCommerce category '{category.name}'")

def create_woocommerce_attrubites(name, slug):
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = 'https://eldrapaints.com/wp-json/wc/v3/products/attributes'
    data = {
        'name': name,
        'slug': slug
    }

    response = requests.post(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)

    if response.status_code == 201:
        return response.json()['id']
    else:
        print('Failed to create attributes')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None
    
def sync_family():
    attributes = ItemFamily.objects.all()

    for attribute in attributes:
        woocommerce_attrubites_id = create_woocommerce_attrubites(attribute.name, attribute.name.lower().replace(' ', '-'))
        if woocommerce_attrubites_id:
            attribute.woocommerce_id=woocommerce_attrubites_id
            attribute.save()
            print(f"Created WooCommerce family '{attribute.name}' with ID {woocommerce_attrubites_id}")

def sync_brand():
    attributes = ItemBrand.objects.all()

    for attribute in attributes:
        woocommerce_attrubites_id = create_woocommerce_attrubites(attribute.name, attribute.name.lower().replace(' ', '-'))
        if woocommerce_attrubites_id:
            attribute.woocommerce_id=woocommerce_attrubites_id
            attribute.save()
            print(f"Created WooCommerce brand '{attribute.name}' with ID {woocommerce_attrubites_id}")


def sync_specs():
    attributes = Specs.objects.all()

    for attribute in attributes:
        woocommerce_attrubites_id = create_woocommerce_attrubites(attribute.description, attribute.description.lower().replace(' ', '-'))
        if woocommerce_attrubites_id:
            attribute.woocommerce_id=woocommerce_attrubites_id
            attribute.save()
            print(f"Created WooCommerce specs '{attribute.description}' with ID {woocommerce_attrubites_id}")

def update_woocommerce_attributes(category_id, name):
    url = f'https://eldrapaints.com/wp-json/wc/v3/products/attributes/{category_id}'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'name': name,
    }

    response = requests.put(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    response.raise_for_status() 
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to update category')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None

def sync_variationheader():
    attributes = VariationsHeader.objects.all()

    for attribute in attributes:
        woocommerce_attrubites_id = create_woocommerce_attrubites(attribute.attribute, attribute.attribute.lower().replace(' ', '-'))
        if woocommerce_attrubites_id:
            attribute.woocommerce_id=woocommerce_attrubites_id
            attribute.save()
            print(f"Created WooCommerce VariationsHeader '{attribute.attribute}' with ID {woocommerce_attrubites_id}")

def sync_unit():
    attributes = UnitOfMeasurment.objects.all()

    for attribute in attributes:
        woocommerce_attrubites_id = create_woocommerce_attrubites(attribute.name, attribute.name.lower().replace(' ', '-'))
        if woocommerce_attrubites_id:
            attribute.woocommerce_id=woocommerce_attrubites_id
            attribute.save()
            print(f"Created WooCommerce unit '{attribute.name}' with ID {woocommerce_attrubites_id}")

def sync_variationsdetail():
    attributes = VariationsDetail.objects.all()

    for attribute in attributes:
        variation = attribute.variation.attribute  
        value = attribute.value
        woocommerce_attribute_id = create_woocommerce_attrubites(variation, value)
        
        if woocommerce_attribute_id:
            attribute.woocommerce_id = woocommerce_attribute_id
            attribute.save()
            print(f"Created WooCommerce attribute '{variation}' with ID {woocommerce_attribute_id}")

def get_existing_woocommerce_item(name):
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = 'https://eldrapaints.com/wp-json/wc/v3/products/'
    response = requests.get(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), params={'search': name})
    if response.status_code == 200:
        items = response.json()
        if items:
            for item in items:
                if item['name'].lower() == name.lower():
                    return item['id']
    return None



def get_woocommerce_tags():
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = 'https://eldrapaints.com/wp-json/wc/v3/products/tags'
    response = requests.get(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch tags')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None


def get_woocommerce_prices():
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = 'https://eldrapaints.com/wp-json/wc/v3/products'
    
    response = requests.get(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        products = response.json()
        prices = [{'id': product['id'], 'name': product['name'], 'price': product['price']} for product in products]
        return prices
    else:
        print('Failed to fetch prices')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None

def create_woocommerce_item(name, slug, category_id, tags, price):
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = 'https://eldrapaints.com/wp-json/wc/v3/products'
    
    data = {
        'name': name,
        'slug': slug,
        'type': 'simple',
        'regular_price': str(price),
        'categories': [{'id': category_id}] if category_id else [],
        'tags': [{'id': tag['id']} for tag in tags] if tags else []
    }
    
    response = requests.post(store_url, json=data, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if response.status_code in [200, 201]:
        return response.json().get('id')
    else:
        print('Failed to create WooCommerce item')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None



def update_woocommerce_item(woocommerce_item_id, name, slug, category_id, tags, price):
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = f'https://eldrapaints.com/wp-json/wc/v3/products/{woocommerce_item_id}'
    
    data = {
        'name': name,
        'slug': slug,
        'categories': [{'id': category_id}],
        'tags': [{'id': tag_id} for tag_id in tags],
        'regular_price': str(price)  
    }

    response = requests.put(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)

    if response.status_code == 200:
        return response.json()['id']
    else:
        print('Failed to update WooCommerce item')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None

import logging

logging.basicConfig(level=logging.DEBUG)

def delete_woocommerce_item(woocommerce_id):
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = f'https://eldrapaints.com/wp-json/wc/v3/products/{woocommerce_id}'

    response = requests.delete(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    logging.debug(f"Request URL: {response.url}")
    logging.debug(f"Request Headers: {response.request.headers}")
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Headers: {response.headers}")
    logging.debug(f"Response Content: {response.content}")

    if response.status_code in [200, 201, 204]:
        return True
    else:
        print('Failed to delete WooCommerce item')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return False


#handle exceptions :
def handle_exception(e):
    if isinstance(e, ObjectDoesNotExist):
        return JsonResponse({"error": "Object not found"}, status=404)
    elif isinstance(e, ValidationError):
        return JsonResponse({"error": e.messages}, status=400)
    elif isinstance(e, HttpError):
        return JsonResponse({"error": str(e)}, status=e.status_code)
    else:
        return JsonResponse({"error": "An unexpected error occurred "}, status=500)

# create and crud functions : 
@api.post("/activity/", response=ActivityIn, tags=["Activity"])
def create_activity(request, payload: ActivityIn):
    try:
        activity = ConcreteActivity.objects.create(
            date_created=payload.date_created,
            date_modified=payload.date_modified,
            time_created=payload.time_created,
        )
        return ActivityIn(
            date_created=activity.date_created,
            date_modified=activity.date_modified,
            time_created=activity.time_created,
        )
    except Exception as e:
        return handle_exception(e)

@api.post("/category/", response=ItemCategoryOut, tags=["Category"])
def create_category(request, payload: ItemCategoryIn):
    try:
        category, created = ItemCategory.objects.update_or_create(
            name=payload.name,
            defaults={
                'image': payload.image,
                'path': payload.path,
                'depth': 0
            }
        )

        if payload.parent:
            parent_category = get_object_or_404(ItemCategory, id=payload.parent)
            category.parentt = parent_category
            category.save()

        try:
            sync_categories()
        except Exception as e:
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
            }, status=500)
        
        return JsonResponse({
            'name': category.name,
            'image': str(category.image.url) if category.image else None,
            'path': category.path,
            'parent': category.parentt.id if category.parentt else None,
            'woocommerce_id': category.woocommerce_id,
        })
    except IntegrityError as e:
        return JsonResponse({
            'error': f"Error creating/updating category: {str(e)}"
        }, status=500)

@api.post("/family/", response=ItemFamilyIn, tags=["Family"])
def create_family(request,payload: ItemFamilyIn):
    try:
        family = ItemFamily.objects.create(
            name=payload.name,
        )
        try:
            sync_family()
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'name': family.name,
            })
    except Exception as e:
        return handle_exception(e)
    
@api.post("/brand/", response=ItemBrandIn, tags=["Brand"])
def create_brand(request,payload: ItemBrandIn):
    try:
        brand = ItemBrand.objects.create(
            name=payload.name,
        )
        try:
            sync_brand()
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'name': brand.name,
            })
    except Exception as e:
        return handle_exception(e)

@api.post("/specs/", response=SpecsIn, tags=["Specs"])
def create_specs(request,payload: SpecsIn):
    try:
        specs = Specs.objects.create(
            description=payload.description,
        )
        try:
            sync_specs()
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'description': specs.description,
            })
    except Exception as e:
        return handle_exception(e)

@api.post("/unitmeasurments/", response=UnitOfMeasurementIn, tags=["Unitmeasurments"])
def create_unitmeasurments(request,payload: UnitOfMeasurementIn):
    try:
        unitmeasurments = UnitOfMeasurment.objects.create(
                name=payload.name,
                code=payload.code,
                type=payload.type
        )
        try:
            sync_unit()
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'name': unitmeasurments.name,
            'code' :unitmeasurments.code,
            'type' :unitmeasurments.type
            })
    except Exception as e:
        return handle_exception(e)

@api.post("/tags/", response=TagsIn, tags=["Tags"])
def create_tags(request,payload: TagsIn):
    try:
        tags = Tags.objects.create(
                name=payload.name,
        )
        try:
            sync_tags()
        except Exception as e :
                        return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
            }, status=500)
        return JsonResponse({
            'name': tags.name,
            'woocommerce_id':tags.woocommerce_id,
            })
    except Exception as e: 
        return handle_exception(e)

@api.post("/VariationsHeader/", response=VariationsHeaderIn, tags=["VariationsHeader"])
def create_VariationsHeader(request,payload: VariationsHeaderIn):
    try:
        VariationsHeaderr = VariationsHeader.objects.create(
        attribute=payload.attribute,
        )
        try:
            sync_variationheader()
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'attribute' :VariationsHeaderr.attribute,
            })
    except Exception as e:
        return handle_exception(e)

@api.post("/VariationsDetail/", response=VariationsDetailIn, tags=["VariationsDetail"])
def create_VariationsDetail(request,payload: VariationsDetailIn):
    try:
        variation=get_object_or_404(VariationsHeader,id=payload.variation_id)
        VariationsDetaill = VariationsDetail.objects.create(
            variation=variation,
            value=payload.value,

        )
        try:
            sync_variationsdetail()
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'variation_id':variation.id,
            'value':VariationsDetaill.value,
            })
    except Exception as e:
        return handle_exception(e)

@api.post("/items/", tags=['Item'])
def create_item(request, data: ItemCreate):
    with transaction.atomic():
        item = Item(
            name=data.name,
            active=data.active,
            status=data.status,
            description=data.description,
            role=data.role,
            sku_code=data.sku_code,
            barcode_type=data.barcode_type,
            barcode=data.barcode,
            type=data.type,
            usage=data.usage,
            is_variant=data.is_variant,
            tracking_stock_by_variant=data.tracking_stock_by_variant,
            returnable_item=data.returnable_item,
            width=data.width,
            width_unit_of_measure=UnitOfMeasurment.objects.filter(id=data.width_unit_of_measure).first() if data.width_unit_of_measure else None,
            height=data.height,
            height_unit_of_measure=UnitOfMeasurment.objects.filter(id=data.height_unit_of_measure).first() if data.height_unit_of_measure else None,
            length=data.length,
            length_unit_of_measure=UnitOfMeasurment.objects.filter(id=data.length_unit_of_measure).first() if data.length_unit_of_measure else None,
            weight=data.weight,
            weight_unit_of_measure=UnitOfMeasurment.objects.filter(id=data.weight_unit_of_measure).first() if data.weight_unit_of_measure else None,
            available_in_pos=data.available_in_pos,
            shelf_life=data.shelf_life,
            end_of_life=data.end_of_life,
            allow_sales=data.allow_sales,
            max_discount_sales=Decimal(data.max_discount_sales) if data.max_discount_sales is not None else None,
            default_sale_unit_of_measure=UnitOfMeasurment.objects.filter(id=data.default_sale_unit_of_measure).first() if data.default_sale_unit_of_measure else None,
            default_selling_price=Decimal(data.default_selling_price) if data.default_selling_price is not None else None,
            default_selling_price_usd=Decimal(data.default_selling_price_usd) if data.default_selling_price_usd is not None else None,
            default_cost=Decimal(data.default_cost) if data.default_cost is not None else None,
            default_cost_usd=Decimal(data.default_cost_usd) if data.default_cost_usd is not None else None,
            lead_time=data.lead_time,
            minimum_quantity_order=data.minimum_quantity_order,
            default_purchase_unit_of_measure=UnitOfMeasurment.objects.filter(id=data.default_purchase_unit_of_measure).first() if data.default_purchase_unit_of_measure else None,
            minimum_quantity_in_stock=data.minimum_quantity_in_stock,
            warranty_period=data.warranty_period,
            allow_negative_stock=data.allow_negative_stock,
            auto_reorder=data.auto_reorder,
            variant_of=Item.objects.filter(id=data.variant_of).first() if data.variant_of else None,
            price=data.price,
            regular_price=data.regular_price,
            sales_price=data.sales_price,
            woocommerce_id=data.woocommerce_id,
        )

        item.save()

        item.unit_of_measure.set(UnitOfMeasurment.objects.filter(id__in=data.unit_of_measure))
        item.tags.set(Tags.objects.filter(id__in=data.tags))
        item.family = ItemFamily.objects.filter(id=data.family_id).first() if data.family_id else None
        item.brand = ItemBrand.objects.filter(id=data.brand_id).first() if data.brand_id else None
        item.category = ItemCategory.objects.filter(id=data.category_id).first() if data.category_id else None
        item.specs.set(Specs.objects.filter(id__in=data.specs_id))
        item.variations.set(VariationsDetail.objects.filter(id__in=data.variations))
        item.selected_variations.set(VariationsDetail.objects.filter(id__in=data.selected_variations))
        item.alternative_items.set(Item.objects.filter(id__in=data.alternative_items))

        item.save()

        if item.tracking_stock_by_variant:
            item.role = 'template'
        elif item.variant_of is not None:
            item.role = 'variant'
        elif item.variant_of is None and not item.tracking_stock_by_variant:
            item.role = 'standalone'

        item.save()

        fields_to_round = ['default_selling_price', 'default_selling_price_usd', 'default_cost', 'default_cost_usd']
        for field_name in fields_to_round:
            field_value = getattr(item, field_name)
            if field_value is not None:
                rounded_value = round_value(Decimal(field_value))
                setattr(item, field_name, rounded_value)
        item.save()

        try:
            existing_woocommerce_id = get_existing_woocommerce_item(item.name)
            woocommerce_category_id = item.category.woocommerce_id if item.category else None
            if not existing_woocommerce_id:
                woocommerce_tags = get_woocommerce_tags()
                woocommerce_price = get_woocommerce_prices()
                woocommerce_item_id = create_woocommerce_item(
                    item.name, 
                    item.name.lower().replace(' ', '-'), 
                    woocommerce_category_id, 
                    woocommerce_tags, 
                    woocommerce_price, 
                )
                if woocommerce_item_id:
                    item.woocommerce_id = woocommerce_item_id
                    item.save()
                    print(f"Created WooCommerce item '{item.name}' with ID {woocommerce_item_id}")
                else:
                    print(f"Failed to create WooCommerce item '{item.name}'")
            else:
                item.woocommerce_id = existing_woocommerce_id
                item.save()
                print(f"Item '{item.name}' already exists in WooCommerce with ID {existing_woocommerce_id}")
        except Exception as e:
            return {"success": False, "error": f"Error syncing with WooCommerce: {str(e)}"}

        return {"success": True, "item_id": item.id}

@api.post("/packages/", response=PackageIn, tags=['Packages'])
def create_package(request, payload: PackageIn):
    try:
        package = Package.objects.create(
            name=payload.name,
            weight=payload.weight,
            length=payload.length,
            height=payload.height,
            width=payload.width,
            material=payload.material  
        )
        return PackageIn(
            name=package.name,
            weight=package.weight,
            length=package.length,
            height=package.height,
            width=package.width,
            material=package.material,
        )
    except Exception as e:
        return handle_exception(e)

@api.post("/item-packages/", response=ItemPackageIn, tags=['Item Packages'])
def create_item_package(request, payload: ItemPackageIn):
    try:
        item = Item.objects.get(id=payload.item_id)
        package = Package.objects.get(id=payload.package_id)

        item_package = ItemPackage.objects.create(
            item=item,
            package=package,
            quantity=payload.quantity,
            barcode=payload.barcode
        )

        return ItemPackageIn(
            item_id=item_package.item.id,
            package_id=item_package.package.id,
            quantity=item_package.quantity,
            barcode=item_package.barcode
        )
    except Exception as e:
        return handle_exception(e)

@api.post("/warehouses/", response=WarehouseIn, tags=['Warehouses'])
def create_warehouse(request, payload: WarehouseIn):
    try:
        warehouse = Warehouse.objects.create(
            name=payload.name,
            country=payload.country,
            city=payload.city,
            address=payload.address,
            branch=payload.branch,
            initial_Data=payload.initial_data,  
            default=payload.default,
            show_room=payload.show_room
        )

        return WarehouseIn(
            name=warehouse.name,
            country=warehouse.country,
            city=warehouse.city,
            address=warehouse.address,
            branch=warehouse.branch,
            initial_data=warehouse.initial_Data,  
            default=warehouse.default,
            show_room=warehouse.show_room
        )
    except Exception as e:
        return handle_exception(e)

@api.post("/items-warehouses/", response=ItemsWarehouseIn, tags=["Items Warehouses"])
def create_items_warehouse(request, payload: ItemsWarehouseIn):
    try:
        warehouse = Warehouse.objects.get(id=payload.warehouse_id)
        item = Item.objects.get(id=payload.item_id)

        items_warehouse = Itemswarehouse.objects.create(
            warehouse=warehouse,
            item=item,
            quantity=payload.quantity,
            net_movement=payload.net_movement,
            quantity_reserved=payload.quantity_reserved,
            branch=payload.branch,
            opening=payload.opening,
            opening_quantity=payload.opening_quantity
        )

        return ItemsWarehouseIn(
            warehouse_id=items_warehouse.warehouse.id,
            item_id=items_warehouse.item.id,
            quantity=items_warehouse.quantity,
            net_movement=items_warehouse.net_movement,
            quantity_reserved=items_warehouse.quantity_reserved,
            branch=items_warehouse.branch,
            opening=items_warehouse.opening,
            opening_quantity=items_warehouse.opening_quantity
        )
    except Exception as e:
        return handle_exception(e)
    
@api.post("/integration/",response=integrateIn,tags=["Integration"])
def create_integration(request,payload : integrateIn):
    try:
        integratee=integrate.objects.create(
            type=payload.type,
            consumer_key=payload.consumer_key,
            secret_key=payload.secret_key,
            active=payload.active,
            description=payload.description
        )
        return integrateIn(
            type=integratee.type,
            consumer_key=integratee.consumer_key,
            secret_key=integratee.secret_key,
            active=integratee.active,
            description=integratee.description
        )
    except Exception as e:
        return handle_exception(e)

@api.delete("/integration/{integration_id}/",response=integrateIn,tags=["Integration"])
def delete_integration(request, integration_id : int):
    integrationn = integrate.objects.filter(id=integration_id).first()
    if not integrationn :
        return HttpResponse(status=404)
    
    integrationn.delete()
    return {"message": "Integrationd deleted successfully"}

@api.put("/integration/{integration_id}/",response=integrateIn,tags=["Integration"])
def update_integrate(request,integration_id : int , payload : integrateIn):
    integratee=get_object_or_404(integrate,id=integration_id)
    integratee.type=payload.type
    integratee.consumer_key=payload.consumer_key
    integratee.secret_key=payload.secret_key
    integratee.active=payload.active
    integratee.description=payload.description


    return integrateIn(
        type=integratee.type,
        consumer_key=integratee.consumer_key,
        secret_key=integratee.secret_key,
        active=integratee.active,
        description=integratee.description,
    )

@api.get("/integration/{integration_id}/",response=integrateIn,tags=["Integration"])
def read_integration(request,integration_id : int):
    try:
        integration=get_object_or_404(integrate,id=integration_id)
        return integrateIn(
            type=integration.type,
            consumer_key=integration.consumer_key,
            secret_key=integration.secret_key,
            active=integration.active,
            description=integration.description,
        )
    except Exception as e :
        return handle_exception(e)

@api.put("/activity/{activity_id}/", response=ActivityIn, tags=["Activity"])
def update_activity(request, activity_id: int, payload: ActivityIn):
    activity = get_object_or_404(ConcreteActivity, id=activity_id)
    for attr, value in payload.dict().items():
        setattr(activity, attr, value)
    activity.save()
    return ActivityIn(
        date_created=activity.date_created,
        date_modified=activity.date_modified,
        time_created=activity.time_created,
    )

@api.delete("/activity/{activity_id}/", response={204: None}, tags=["Activity"])
def delete_activity(request, activity_id: int):
    activity = get_object_or_404(ConcreteActivity, id=activity_id)
    activity.delete()
    return {"message": "Activity deleted successfully"}

@api.put("/category/{category_id}/", response=ItemCategoryOut, tags=["Category"])
def update_category(request, category_id: int, payload: ItemCategoryIn):
    category = get_object_or_404(ItemCategory, id=category_id)
    

    for attr, value in payload.dict(exclude={"parent"}).items():
        setattr(category, attr, value)
    

    if payload.parent:
        parent_category = get_object_or_404(ItemCategory, id=payload.parent)
        category.parentt = parent_category
    else:
        category.parentt = None
    
    category.save()

    try:
        update_response = update_woocommerce_category(category.woocommerce_id, category.name, category.path)
        if update_response:
            print(f"Updated WooCommerce category '{category.name}'")
        else:
            print(f"Failed to update WooCommerce category '{category.name}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)

    return ItemCategoryOut(
        name=category.name,
        image=str(category.image.url) if category.image else None,
        path=category.path,
        parent=category.parentt.id if category.parentt else None,
        woocommerce_id=category.woocommerce_id
    )

@api.delete("/category/{category_id}/{woocommerce_id}/", tags=['Category'])
def delete_category(request, category_id: int, woocommerce_id: int):

    woocommerce_success, woocommerce_error = delete_woocommerce_category(woocommerce_id)
    if not woocommerce_success:
        return JsonResponse({
            "success": False,
            "message": f"Error deleting category in WooCommerce: {woocommerce_error}"
        }, status=400)
    

    django_success, django_error = delete_django_category(category_id)
    if not django_success:
        return JsonResponse({
            "success": False,
            "message": f"Error deleting category in Django: {django_error}"
        }, status=400)
    
    return JsonResponse({"success": True})

    

@api.put("/family/{family_id}/", response=ItemFamilyIn, tags=["Family"])
def update_family(request, family_id: int, payload: ItemFamilyIn):
    family = get_object_or_404(ItemFamily, id=family_id)
    for attr, value in payload.dict().items():
        setattr(family, attr, value)
    family.save()
    try:
        update_response = update_woocommerce_attributes(family.woocommerce_id, family.name)
        if update_response:
            print(f"Updated WooCommerce family '{family.name}'")
        else:
            print(f"Failed to update WooCommerce family '{family.name}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)
    return ItemFamilyIn(
        name=family.name,
        woocommerce_id=family.woocommerce_id,
    )

@api.delete("/family/{family_id}/", response={204: None}, tags=["Family"])
def delete_family(request, family_id: int):
    family = get_object_or_404(ItemFamily, id=family_id)
    family.delete()
    return {"message": "Family deleted successfully"}

@api.put("/brand/{brand_id}/", response=ItemBrandIn, tags=["Brand"])
def update_brand(request, brand_id: int, payload: ItemBrandIn):
    brand = get_object_or_404(ItemBrand, id=brand_id)
    for attr, value in payload.dict().items():
        setattr(brand, attr, value)
    brand.save()
    try:
        update_response = update_woocommerce_attributes(brand.woocommerce_id, brand.name)
        if update_response:
            print(f"Updated WooCommerce brand '{brand.name}'")
        else:
            print(f"Failed to update WooCommerce brand '{brand.name}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)
    return ItemBrandIn(
        name=brand.name,
        woocommerce_id=brand.woocommerce_id,
    )

@api.delete("/brand/{brand_id}/", response={204: None}, tags=["Brand"])
def delete_brand(request, brand_id: int):
    brand = get_object_or_404(ItemBrand, id=brand_id)
    brand.delete()
    return {"message": "Brand deleted successfully"}
    
@api.put("/specs/{specs_id}/", response=SpecsIn, tags=["Specs"])
def update_specs(request, specs_id: int, payload: SpecsIn):
    specs = get_object_or_404(Specs, id=specs_id)
    for attr, value in payload.dict().items():
        setattr(specs, attr, value)
    specs.save()
    try:
        update_response = update_woocommerce_attributes(specs.woocommerce_id, specs.description)
        if update_response:
            print(f"Updated WooCommerce specs '{specs.description}'")
        else:
            print(f"Failed to update WooCommerce specs '{specs.description}'")
    except Exception as e:
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
            }, status=500)
    return SpecsIn(
        description=specs.description,
        woocommerce_id=specs.woocommerce_id,
    )

@api.delete("/specs/{specs_id}/", response={204: None}, tags=["Specs"])
def delete_specs(request, specs_id: int):
    specs = get_object_or_404(Specs, id=specs_id)
    specs.delete()
    return {"message": "Specs deleted successfully"}

@api.put("/unitmeasurments/{unit_id}/", response=UnitOfMeasurementIn, tags=["Unitmeasurments"])
def update_unitmeasurments(request, unit_id: int, payload: UnitOfMeasurementIn):
    unit = get_object_or_404(UnitOfMeasurment, id=unit_id)
    for attr, value in payload.dict().items():
        setattr(unit, attr, value)
    unit.save()
    try:
        update_response = update_woocommerce_attributes(unit.woocommerce_id, unit.name)
        if update_response:
            print(f"Updated WooCommerce unit '{unit.name}'")
        else:
            print(f"Failed to update WooCommerce unit '{unit.name}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)
    return UnitOfMeasurementIn(
        name=unit.name,
        woocommerce_id=unit.woocommerce_id,
        code=unit.code,
        type=unit.type
    )

@api.delete("/unitmeasurments/{unit_id}/", response={204: None}, tags=["Unitmeasurments"])
def delete_unitmeasurments(request, unit_id: int):
    unit = get_object_or_404(UnitOfMeasurment, id=unit_id)
    unit.delete()
    return {"message": "Unitmeasurments deleted successfully"}

@api.get("/tags/{tags_id}/", response=TagsIn, tags=["Tags"])
def read_tags(request, tags_id: int):
    tags = get_object_or_404(Tags, id=tags_id)
    return TagsIn(
        name=tags.name,
        woocommerce_id=tags.woocommerce_id
    )

@api.delete("/tags/{tags_id}/", response={204: None}, tags=["Tags"])
def delete_tags(request, tags_id: int):
    tags = get_object_or_404(Tags, id=tags_id)
    tags.delete()
    return {"message": "Tags deleted successfully"}

@api.get("/VariationsHeader/{header_id}/", response=VariationsHeaderIn, tags=["VariationsHeader"])
def read_variations_header(request, header_id: int):
    header = get_object_or_404(VariationsHeader, id=header_id)
    return VariationsHeaderIn(
        attribute=header.attribute,
        woocommerce_id=header.woocommerce_id
    )

@api.put("/VariationsHeader/{header_id}/", response=VariationsHeaderIn, tags=["VariationsHeader"])
def update_variations_header(request, header_id: int, payload: VariationsHeaderIn):
    header = get_object_or_404(VariationsHeader, id=header_id)
    for attr, value in payload.dict().items():
        setattr(header, attr, value)
    header.save()
    try:
        update_response = update_woocommerce_attributes(header.woocommerce_id, header.attribute)
        if update_response:
            print(f"Updated WooCommerce header '{header.attribute}'")
        else:
            print(f"Failed to update WooCommerce header '{header.attribute}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)
    return VariationsHeaderIn(
        attribute=header.attribute,
        woocommerce_id=header.woocommerce_id,
    )

@api.delete("/VariationsHeader/{header_id}/", response={204: None}, tags=["VariationsHeader"])
def delete_variations_header(request, header_id: int):
    header = get_object_or_404(VariationsHeader, id=header_id)
    header.delete()
    return {"message": "VariationsHeader deleted successfully"}

@api.get("/VariationsDetail/{detail_id}/", response=VariationsDetailIn, tags=["VariationsDetail"])
def read_variations_detail(request, detail_id: int):
    detail = get_object_or_404(VariationsDetail, id=detail_id)
    return VariationsDetailIn(
        variation_id=detail.variation.id,
        value=detail.value,
        woocommerce_id=detail.woocommerce_id
    )

@api.put("/VariationsDetail/{detail_id}/", response=VariationsDetailIn, tags=["VariationsDetail"])
def update_variations_detail(request, detail_id: int, payload: VariationsDetailIn):
    detail = get_object_or_404(VariationsDetail, id=detail_id)
    variation = get_object_or_404(VariationsHeader, id=payload.variation_id)
    detail.variation = variation
    detail.value = payload.value
    detail.save()
    try:
        update_response = update_woocommerce_attributes(detail.woocommerce_id, detail.value)
        if update_response:
            print(f"Updated WooCommerce detail '{detail.value}'")
        else:
            print(f"Failed to update WooCommerce detail '{detail.value}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)
    return VariationsDetailIn(
        variation_id=detail.variation.id,
        value=detail.value,
        woocommerce_id=detail.woocommerce_id,
    )

@api.delete("/VariationsDetail/{detail_id}/", response={204: None}, tags=["VariationsDetail"])
def delete_variations_detail(request, detail_id: int):
    detail = get_object_or_404(VariationsDetail, id=detail_id)
    detail.delete()
    return {"message": "VariationsDetail deleted successfully"}

@api.put("/items/{item_id}/", tags=['Item'])
def update_item(request, item_id: int, data: ItemCreate):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return {"success": False, "error": "Item not found"}

    with transaction.atomic():
        if data.name is not None:
            item.name = data.name
        if data.active is not None:
            item.active = data.active
        if data.status is not None:
            item.status = data.status
        if data.description is not None:
            item.description = data.description
        if data.role is not None:
            item.role = data.role
        if data.sku_code is not None:
            item.sku_code = data.sku_code
        if data.barcode_type is not None:
            item.barcode_type = data.barcode_type
        if data.barcode is not None:
            item.barcode = data.barcode
        if data.type is not None:
            item.type = data.type
        if data.usage is not None:
            item.usage = data.usage
        if data.is_variant is not None:
            item.is_variant = data.is_variant
        if data.tracking_stock_by_variant is not None:
            item.tracking_stock_by_variant = data.tracking_stock_by_variant
        if data.returnable_item is not None:
            item.returnable_item = data.returnable_item
        if data.width is not None:
            item.width = data.width
        if data.width_unit_of_measure is not None:
            item.width_unit_of_measure = UnitOfMeasurment.objects.filter(id=data.width_unit_of_measure).first()
        if data.height is not None:
            item.height = data.height
        if data.height_unit_of_measure is not None:
            item.height_unit_of_measure = UnitOfMeasurment.objects.filter(id=data.height_unit_of_measure).first()
        if data.length is not None:
            item.length = data.length
        if data.length_unit_of_measure is not None:
            item.length_unit_of_measure = UnitOfMeasurment.objects.filter(id=data.length_unit_of_measure).first()
        if data.weight is not None:
            item.weight = data.weight
        if data.weight_unit_of_measure is not None:
            item.weight_unit_of_measure = UnitOfMeasurment.objects.filter(id=data.weight_unit_of_measure).first()
        if data.available_in_pos is not None:
            item.available_in_pos = data.available_in_pos
        if data.shelf_life is not None:
            item.shelf_life = data.shelf_life
        if data.end_of_life is not None:
            item.end_of_life = data.end_of_life
        if data.allow_sales is not None:
            item.allow_sales = data.allow_sales
        if data.max_discount_sales is not None:
            item.max_discount_sales = Decimal(data.max_discount_sales)
        if data.default_sale_unit_of_measure is not None:
            item.default_sale_unit_of_measure = UnitOfMeasurment.objects.filter(id=data.default_sale_unit_of_measure).first()
        if data.default_selling_price is not None:
            item.default_selling_price = Decimal(data.default_selling_price)
        if data.default_selling_price_usd is not None:
            item.default_selling_price_usd = Decimal(data.default_selling_price_usd)
        if data.default_cost is not None:
            item.default_cost = Decimal(data.default_cost)
        if data.default_cost_usd is not None:
            item.default_cost_usd = Decimal(data.default_cost_usd)
        if data.lead_time is not None:
            item.lead_time = data.lead_time
        if data.minimum_quantity_order is not None:
            item.minimum_quantity_order = data.minimum_quantity_order
        if data.default_purchase_unit_of_measure is not None:
            item.default_purchase_unit_of_measure = UnitOfMeasurment.objects.filter(id=data.default_purchase_unit_of_measure).first()
        if data.minimum_quantity_in_stock is not None:
            item.minimum_quantity_in_stock = data.minimum_quantity_in_stock
        if data.warranty_period is not None:
            item.warranty_period = data.warranty_period
        if data.allow_negative_stock is not None:
            item.allow_negative_stock = data.allow_negative_stock
        if data.auto_reorder is not None:
            item.auto_reorder = data.auto_reorder
        if data.variant_of is not None:
            item.variant_of = Item.objects.filter(id=data.variant_of).first()
        if data.price is not None:
            item.price = data.price
        if data.regular_price is not None:
            item.regular_price = data.regular_price
        if data.sales_price is not None:
            item.sales_price = data.sales_price

        item.save()

        if data.unit_of_measure:
            item.unit_of_measure.set(UnitOfMeasurment.objects.filter(id__in=data.unit_of_measure))
        if data.tags:
            item.tags.set(Tags.objects.filter(id__in=data.tags))
        if data.family_id:
            item.family = ItemFamily.objects.filter(id=data.family_id).first()
        if data.brand_id:
            item.brand = ItemBrand.objects.filter(id=data.brand_id).first()
        if data.category_id:
            item.category = ItemCategory.objects.filter(id=data.category_id).first()
        if data.specs_id:
            item.specs.set(Specs.objects.filter(id__in=data.specs_id))
        if data.variations:
            item.variations.set(VariationsDetail.objects.filter(id__in=data.variations))
        if data.selected_variations:
            item.selected_variations.set(VariationsDetail.objects.filter(id__in=data.selected_variations))
        if data.alternative_items:
            item.alternative_items.set(Item.objects.filter(id__in=data.alternative_items))

        item.save()

        if item.tracking_stock_by_variant:
            item.role = 'template'
        elif item.variant_of is not None:
            item.role = 'variant'
        elif item.variant_of is None and not item.tracking_stock_by_variant:
            item.role = 'standalone'

        item.save()

        fields_to_round = ['default_selling_price', 'default_selling_price_usd', 'default_cost', 'default_cost_usd']
        for field_name in fields_to_round:
            field_value = getattr(item, field_name)
            if field_value is not None:
                rounded_value = round_value(Decimal(field_value))
                setattr(item, field_name, rounded_value)
        item.save()


        try:
            woocommerce_item_id = item.woocommerce_id
            if woocommerce_item_id:
                woocommerce_category_id = item.category.woocommerce_id if item.category else None
                woocommerce_tags = [tag.woocommerce_id for tag in item.tags.all()]
                
                update_woocommerce_item(woocommerce_item_id, item.name, item.name.lower().replace(' ', '-'), woocommerce_category_id, woocommerce_tags, item.price)
                print(f"Updated WooCommerce item '{item.name}' with ID {woocommerce_item_id}")
            else:
                woocommerce_category_id = item.category.woocommerce_id if item.category else None
                woocommerce_tags = [tag.woocommerce_id for tag in item.tags.all()]
                
                woocommerce_item_id = create_woocommerce_item(item.name, item.name.lower().replace(' ', '-'), woocommerce_category_id, woocommerce_tags, item.price)
                if woocommerce_item_id:
                    item.woocommerce_id = woocommerce_item_id
                    item.save()
                    print(f"Created WooCommerce item '{item.name}' with ID {woocommerce_item_id}")
        except Exception as e:
            return {"success": False, "error": f"Error syncing with WooCommerce: {str(e)}"}

        return {"success": True, "item_id": item.id}

@api.delete("/items/{item_id}/{woocommerce_id}/", tags=['Item'])
def delete_item(request, item_id: int = Path(...), woocommerce_id: int = Path(...)):
    try:
        if item_id:
            item = get_object_or_404(Item, id=item_id)
            with transaction.atomic():
                item.delete()

        if woocommerce_id:
            try:
                success = delete_woocommerce_item(woocommerce_id)
                if success:
                    return {"success": True, "message": "Item deleted successfully"}
                else:
                    return {"success": False, "message": "Failed to delete item from WooCommerce"}
            except Exception as e:
                return {"success": False, "message": f"Error deleting item from WooCommerce: {str(e)}"}
        else:
            return {"success": True, "message": "Item deleted successfully from Django"}
    except Exception as e:
        return {"success": False, "message": f"Error deleting item: {str(e)}"}

@api.get("/activity/{activity_id}/", response=ActivityIn, tags=["Activity"])
def read_activity(request, activity_id: int):
    activity = get_object_or_404(ConcreteActivity, id=activity_id)
    return ActivityIn(
        date_created=activity.date_created,
        date_modified=activity.date_modified,
        time_created=activity.time_created,
    )

@api.get("/category/{category_id}/", response=ItemCategoryIn, tags=['Category'])
def read_category(request, category_id: int):
    category = get_object_or_404(ItemCategory, id=category_id)
    return ItemCategoryIn(
        name=category.name,
        image=category.image.url, 
        path=category.path,
        woocommerce_id=category.woocommerce_id,
    )

@api.get("/family/{family_id}/", response=ItemFamilyIn, tags=["Family"])
def read_family(request, family_id: int):
    family = get_object_or_404(ItemFamily, id=family_id)
    return ItemFamilyIn(
        name=family.name,
        woocommerce_id=family.woocommerce_id,
    )

@api.get("/brand/{brand_id}/", response=ItemBrandIn, tags=["Brand"])
def read_brand(request, brand_id: int):
    brand = get_object_or_404(ItemBrand, id=brand_id)
    return ItemBrandIn(
        name=brand.name,
        woocommerce_id=brand.woocommerce_id
    )

@api.get("/specs/{specs_id}/", response=SpecsIn, tags=["Specs"])
def read_specs(request, specs_id: int):
    specs = get_object_or_404(Specs, id=specs_id)
    return SpecsIn(
        description=specs.description,
        woocommerce_id=specs.woocommerce_id
    )

@api.get("/unitmeasurments/{unit_id}/", response=UnitOfMeasurementIn, tags=["Unitmeasurments"])
def read_unitmeasurments(request, unit_id: int):
    unit = get_object_or_404(UnitOfMeasurment, id=unit_id)
    return UnitOfMeasurementIn(
        name=unit.name,
        code=unit.code,
        type=unit.type,
        woocommerce_id=unit.woocommerce_id
    )

@api.put("/tags/{tags_id}/", response=TagsIn, tags=["Tags"])
def update_tags(request, tags_id: int, payload: TagsIn):
    tags = get_object_or_404(Tags, id=tags_id)
    for attr, value in payload.dict().items():
        setattr(tags, attr, value)
    tags.save()
    try:
        update_response=update_woocommerce_tag(tags.woocommerce_id,tags.name)
        if update_response:
            print(f"Updated WooCommerce tag '{tags.name}'")
        else:
            print(f"Failed to update WooCommerce tag for'{tags.name}'")
    except Exception as e:
        return JsonResponse({
            'error': f"Error syncing with WooCommerce: {str(e)}"
        }, status=500)
    return TagsIn(
        name=tags.name,
        woocommerce_id=tags.woocommerce_id,
    )

@api.get("/items/{item_id}", response=ItemOut,tags=['Item'])
def read_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)

    item_out_data = {
        "id": item.id,
        "name": item.name,
        "active": item.active,
        "description": item.description,
        "role": item.role,
        "sku_code": item.sku_code,
        "barcode_type": item.barcode_type,
        "barcode": item.barcode,
        "type": item.type,
        "usage": item.usage,
        "unit_of_measure": [um.id for um in item.unit_of_measure.all()],
        "tags": [tag.id for tag in item.tags.all()],
        "family_id": item.family_id if item.family_id else None,
        "brand_id": item.brand_id if item.brand_id else None,
        "category_id": item.category_id if item.category_id else None,
        "specs_id": [spec.id for spec in item.specs.all()],
        "is_variant": item.is_variant,
        "tracking_stock_by_variant": item.tracking_stock_by_variant,
        "variations": [var.id for var in item.variations.all()],
        "selected_variations": [var.id for var in item.selected_variations.all()],
        "alternative_items": [alt_item.id for alt_item in item.alternative_items.all()],
        "returnable_item": item.returnable_item,
        "width": item.width,
        "width_unit_of_measure": item.width_unit_of_measure.id if item.width_unit_of_measure else None,
        "height": item.height,
        "height_unit_of_measure": item.height_unit_of_measure.id if item.height_unit_of_measure else None,
        "length": item.length,
        "length_unit_of_measure": item.length_unit_of_measure.id if item.length_unit_of_measure else None,
        "weight": item.weight,
        "weight_unit_of_measure": item.weight_unit_of_measure.id if item.weight_unit_of_measure else None,
        "available_in_pos": item.available_in_pos,
        "shelf_life": item.shelf_life,
        "end_of_life": item.end_of_life,
        "allow_sales": item.allow_sales,
        "max_discount_sales": item.max_discount_sales,
        "default_sale_unit_of_measure": item.default_sale_unit_of_measure.id if item.default_sale_unit_of_measure else None,
        "default_selling_price": item.default_selling_price,
        "default_selling_price_usd": item.default_selling_price_usd,
        "default_cost": item.default_cost,
        "default_cost_usd": item.default_cost_usd,
        "lead_time": item.lead_time,
        "minimum_quantity_order": item.minimum_quantity_order,
        "default_purchase_unit_of_measure": item.default_purchase_unit_of_measure.id if item.default_purchase_unit_of_measure else None,
        "minimum_quantity_in_stock": item.minimum_quantity_in_stock,
        "warranty_period": item.warranty_period,
        "allow_negative_stock": item.allow_negative_stock,
        "auto_reorder": item.auto_reorder,
        "variant_of": item.variant_of.id if item.variant_of else None,
        "price": item.price,
        "regular_price": item.regular_price,
        "sales_price": item.sales_price,
        "woocommerce_id":item.woocommerce_id,
    }

    item_out = ItemOut(**item_out_data)
    return item_out

@api.get("/packages/{package_id}/", response=PackageIn, tags=["Packages"])
def read_package(request, package_id: int):
    package = Package.objects.get(id=package_id)
    return PackageIn(
        name=package.name,
        weight=package.weight,
        length=package.length,
        height=package.height,
        width=package.width,
        material=package.material
    )

@api.get("/item-packages/{item_package_id}/", response=ItemPackageIn, tags=["Item Packages"])
def read_item_package(request, item_package_id: int):
    item_package = ItemPackage.objects.get(id=item_package_id)
    return ItemPackageIn(
        item_id=item_package.item.id,
        package_id=item_package.package.id,
        quantity=item_package.quantity,
        barcode=item_package.barcode
    )

@api.get("/warehouses/{warehouse_id}/", response=WarehouseIn, tags=["Warehouses"])
def read_warehouse(request, warehouse_id: int):
    warehouse = Warehouse.objects.get(id=warehouse_id)
    return WarehouseIn(
        name=warehouse.name,
        country=warehouse.country,
        city=warehouse.city,
        address=warehouse.address,
        branch=warehouse.branch,
        initial_data=warehouse.initial_Data,  
        default=warehouse.default,
        show_room=warehouse.show_room
    )

@api.get("/items-warehouses/{items_warehouse_id}/", response=ItemsWarehouseIn, tags=["Items Warehouses"])
def read_items_warehouse(request, items_warehouse_id: int):
    items_warehouse = Itemswarehouse.objects.get(id=items_warehouse_id)
    return ItemsWarehouseIn(
        warehouse_id=items_warehouse.warehouse.id,
        item_id=items_warehouse.item.id,
        quantity=items_warehouse.quantity,
        net_movement=items_warehouse.net_movement,
        quantity_reserved=items_warehouse.quantity_reserved,
        branch=items_warehouse.branch,
        opening=items_warehouse.opening,
        opening_quantity=items_warehouse.opening_quantity
    )

@api.put("/packages/{package_id}/", response=PackageIn, tags=["Packages"])
def update_package(request, package_id: int, payload: PackageIn):
    package = Package.objects.get(id=package_id)
    package.name = payload.name
    package.weight = payload.weight
    package.length = payload.length
    package.height = payload.height
    package.width = payload.width
    package.material = payload.material
    package.save()

    return PackageIn(
        name=package.name,
        weight=package.weight,
        length=package.length,
        height=package.height,
        width=package.width,
        material=package.material
    )

@api.put("/item-packages/{item_package_id}/", response=ItemPackageIn, tags=["Item Packages"])
def update_item_package(request, item_package_id: int, payload: ItemPackageIn):
    item_package = ItemPackage.objects.get(id=item_package_id)
    item_package.quantity = payload.quantity
    item_package.barcode = payload.barcode
    item_package.save()

    return ItemPackageIn(
        item_id=item_package.item.id,
        package_id=item_package.package.id,
        quantity=item_package.quantity,
        barcode=item_package.barcode
    )

@api.put("/warehouses/{warehouse_id}/", response=WarehouseIn, tags=["Warehouses"])
def update_warehouse(request, warehouse_id: int, payload: WarehouseIn):
    warehouse = Warehouse.objects.get(id=warehouse_id)
    warehouse.name = payload.name
    warehouse.country = payload.country
    warehouse.city = payload.city
    warehouse.address = payload.address
    warehouse.branch = payload.branch
    warehouse.initial_Data = payload.initial_data
    warehouse.default = payload.default
    warehouse.show_room = payload.show_room
    warehouse.save()

    return WarehouseIn(
        name=warehouse.name,
        country=warehouse.country,
        city=warehouse.city,
        address=warehouse.address,
        branch=warehouse.branch,
        initial_data=warehouse.initial_Data,  
        default=warehouse.default,
        show_room=warehouse.show_room
    )

@api.put("/items-warehouses/{items_warehouse_id}/", response=ItemsWarehouseIn, tags=["Items Warehouses"])
def update_items_warehouse(request, items_warehouse_id: int, payload: ItemsWarehouseIn):
    items_warehouse = Itemswarehouse.objects.get(id=items_warehouse_id)
    items_warehouse.quantity = payload.quantity
    items_warehouse.net_movement = payload.net_movement
    items_warehouse.quantity_reserved = payload.quantity_reserved
    items_warehouse.branch = payload.branch
    items_warehouse.opening = payload.opening
    items_warehouse.opening_quantity = payload.opening_quantity
    items_warehouse.save()

    return ItemsWarehouseIn(
         warehouse_id=items_warehouse.warehouse.id,
        item_id=items_warehouse.item.id,
        quantity=items_warehouse.quantity,
        net_movement=items_warehouse.net_movement,
        quantity_reserved=items_warehouse.quantity_reserved,
        branch=items_warehouse.branch,
        opening=items_warehouse.opening,
        opening_quantity=items_warehouse.opening_quantity
    )

@api.delete("/packages/{package_id}/", tags=["Packages"])
def delete_package(request, package_id: int):
    package = Package.objects.get(id=package_id)
    package.delete()
    return {"message": "Package deleted successfully"}

@api.delete("/item-packages/{item_package_id}/", tags=["Item Packages"])
def delete_item_package(request, item_package_id: int):
    item_package = ItemPackage.objects.get(id=item_package_id)
    item_package.delete()
    return {"message": "Item Package deleted successfully"}

@api.delete("/warehouses/{warehouse_id}/", tags=["Warehouses"])
def delete_warehouse(request, warehouse_id: int):
    warehouse = Warehouse.objects.get(id=warehouse_id)
    warehouse.delete()
    return {"message": "Warehouse deleted successfully"}

@api.delete("/items-warehouses/{items_warehouse_id}/", tags=["Items Warehouses"])
def delete_items_warehouse(request, items_warehouse_id: int):
    items_warehouse = Itemswarehouse.objects.get(id=items_warehouse_id)
    items_warehouse.delete()
    return {"message": "Items Warehouse deleted successfully"}

#other features :

@api.get("/integrations/{integration_id}/activated/",tags=["Integration"])
def activated_integration(request, integration_id: int):
    integration = integrate.objects.get(id=integration_id)
    if integration.active == True:
        return {"error": f"The integration {integration_id} is already activated"}
    elif integration.active == False:
        integration.active = True
        integration.save()
        return {"message": f"Integration {integration_id} activated successfully"}

@api.get("/integrations/{integration_id}/desactivated/reactivated",tags=["Integration"])
def desactivated_reactivated_integration(request, integration_id: int):
    integration = integrate.objects.get(id=integration_id)
    if integration.active == True:
        integration.active = False
        integration.save()
        return {"message": f"Integration {integration_id} desactivated"}
    elif integration.active == False:
        integration.active = True
        integration.save()
        return {"message": f"Integration {integration_id} reactivated successfully you can't create new warehouse" }

@api.get("/items/",tags=['Item'])
def list_items(request):
    site_url = 'https://eldrapaints.com/wp-json/wc/v3/products'
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    params = {
        'per_page': 100, 
    }

    response = requests.get(site_url, auth=(consumer_key, consumer_secret), params=params)
    if response.status_code == 200:
        items = response.json()
        return {"success": True, "items": items}
    else:
        return {"success": False, "message": f"Failed to fetch items: {response.status_code}", "response": response.json()}
    
@api.get("/categories",tags=['Category'])
def list_categories(request):
    site_url = 'https://eldrapaints.com/wp-json/wc/v3/products/categories'
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'

    params = {
        'per_page': 100, 
    }

    response = requests.get(site_url, auth=(consumer_key, consumer_secret), params=params)

    if response.status_code == 200:
        categories = response.json()
        return {"success": True, "categories": categories}
    else:
        return {"success": False, "message": f"Failed to fetch categories: {response.status_code}", "response": response.json()}

@api.post("/duplicate-woocommerce-product/{item_id}/", tags=["Item"])
def duplicate_woocommerce_product(request, item_id: int):
    consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
    consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
    store_url = 'https://eldrapaints.com/wp-json/wc/v3/products/'

    item = get_object_or_404(Item, id=item_id)
    woocommerce_id = item.woocommerce_id

    if not woocommerce_id:
        return {"success": False, "error": "Item does not have a WooCommerce ID"}

    try:
        response = requests.post(f'{store_url}{woocommerce_id}/duplicate', auth=HTTPBasicAuth(consumer_key, consumer_secret))

        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        elif response.status_code == 404:
            return {
                'success': False,
                'error': f'Product with WooCommerce ID {woocommerce_id} not found in WooCommerce. Status Code: 404'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to duplicate product. Status Code: {response.status_code}',
                'response': response.json()
            }

    except Exception as e:
        return {
            'success': False,
            'error': f"Error duplicating product: {str(e)}"
        }