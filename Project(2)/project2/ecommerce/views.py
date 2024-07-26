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
from requests.auth import HTTPBasicAuth
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
api = NinjaAPI()
#Convert datetime to string :
def convert_datetime_to_string(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None

#Woocommerce Integration Functions : 

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
    
def create_woocommerce_customer(name, email):
    url = 'https://eldrapaints.com/wp-json/wc/v3/customers'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'email': email,
        'first_name': name,
        'username': email, 
        'password': 'password123'  
    }

    response = requests.post(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print('Failed to create WooCommerce customer')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None

def update_woocommerce_customer(customer_id, name, email):
    url = f'https://eldrapaints.com/wp-json/wc/v3/customers/{customer_id}'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"

    data = {
        'email': email,
        'first_name': name,
        'username' : email
    }

    try:
        response = requests.put(
            url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            json=data
        )
        response.raise_for_status()
        return True  
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False  
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return False  

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

def update_woocommerce_order(order_id,number):
    url = f'https://eldrapaints.com/wp-json/wc/v3/orders/{order_id}'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"

    data = {
                'number' : number  ,

    }

    try:
        response = requests.put(
            url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            json=data
        )
        response.raise_for_status()
        return True  
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False  
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return False  

def create_woocommerce_order(number,status,total):
    url = 'https://eldrapaints.com/wp-json/wc/v3/orders'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"
    
    data = {
        'number' : number  ,
        'status':status ,
        'total': total
    }

    response = requests.post(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print('Failed to create WooCommerce orders')
        print('Status Code:', response.status_code)
        print('Response Headers:', response.headers)
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response content is not valid JSON:', response.content)
        return None

def delete_woocommerce_order(order_id):
    url = f'https://eldrapaints.com/wp-json/wc/v3/orders/{order_id}'
    consumer_key = "ck_b905c5395fbfee15c4683104e148918bb31f1739"
    consumer_secret = "cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b"

    try:
        response = requests.delete(
            url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret)
        )
        response.raise_for_status()
        print(f"DELETE request status code: {response.status_code}")
        print(f"DELETE request response: {response.text}")  # Print the response content for debugging
        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return False

#Handle Exceptions :


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

# Activity :
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

@api.get("/activity/{activity_id}/", response=ActivityIn, tags=["Activity"])
def read_activity(request, activity_id: int):
    activity = get_object_or_404(ConcreteActivity, id=activity_id)
    return ActivityIn(
        date_created=activity.date_created,
        date_modified=activity.date_modified,
        time_created=activity.time_created,
    )

# Category :
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
            woocommerce_category_id = create_woocommerce_category(category.name, category.name.lower().replace(' ', '-'))
            if woocommerce_category_id:
                category.woocommerce_id = woocommerce_category_id
                category.save()
                print(f"Created WooCommerce category '{category.name}' with ID {woocommerce_category_id}")
            else:
                print(f"Failed to create WooCommerce category for '{category.name}'")
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

@api.get("/category/{category_id}/", response=ItemCategoryIn, tags=['Category'])
def read_category(request, category_id: int):
    category = get_object_or_404(ItemCategory, id=category_id)
    return ItemCategoryIn(
        name=category.name,
        image=category.image.url, 
        path=category.path,
        woocommerce_id=category.woocommerce_id,
    )

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

@api.get("/category/{category_id}/", response=ItemCategoryIn, tags=['Category'])
def read_category(request, category_id: int):
    category = get_object_or_404(ItemCategory, id=category_id)
    return ItemCategoryIn(
        name=category.name,
        image=category.image.url, 
        path=category.path,
        woocommerce_id=category.woocommerce_id,
    )

@api.get("/category/parents/{name}", response=List[ItemCategoryOut],tags=['Category'])
def get_parent_categories(request, name: str):
    category = get_object_or_404(ItemCategory, name=name)
    parents = []
    parent = category.parentt
    while parent:
        parents.append(parent)
        parent = parent.parentt

    parent_categories = [
        ItemCategoryOut(
            name=parent.name,
            image=parent.image.url if parent.image else None,
            path=str(parent.path),
            parent=parent.parentt.id if parent.parentt else None,
            woocommerce_id=parent.woocommerce_id
        ) for parent in parents
    ]
    
    return parent_categories

#Family :

@api.post("/family/", response=ItemFamilyIn, tags=["Family"])
def create_family(request,payload: ItemFamilyIn):
    try:
        family = ItemFamily.objects.create(
            name=payload.name,
        )
        try:
            woocommerce_family_id=create_woocommerce_attrubites(family.name,family.name.lower().replace(' ', '-'))
            if woocommerce_family_id:
                family.woocommerce_id = woocommerce_family_id
                family.save()
                print(f"Created WooCommerce family '{family.name}' with ID {woocommerce_family_id}")
            else:
                print(f"Failed to create WooCommerce family for '{family.name}'")
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'name': family.name,
            })
    except Exception as e:
        return handle_exception(e)

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

@api.get("/family/", response=List[ItemFamilyOut], tags=["Family"])
def list_all_family(request):
    family = ItemFamily.objects.values('name', 'woocommerce_id')
    return list(family)

@api.get("/family/{family_id}/", response=ItemFamilyIn, tags=["Family"])
def read_family(request, family_id: int):
    family = get_object_or_404(ItemFamily, id=family_id)
    return ItemFamilyIn(
        name=family.name,
        woocommerce_id=family.woocommerce_id,
    )
# Brand :

@api.post("/brand/", response=ItemBrandIn, tags=["Brand"])
def create_brand(request,payload: ItemBrandIn):
    try:
        brand = ItemBrand.objects.create(
            name=payload.name,
        )
        try:
            woocommerce_brand_id=create_woocommerce_attrubites(brand.name,brand.name.lower().replace(' ', '-'))
            if woocommerce_brand_id:
                brand.woocommerce_id = woocommerce_brand_id
                brand.save()
                print(f"Created WooCommerce brand '{brand.name}' with ID {woocommerce_brand_id}")
            else:
                print(f"Failed to create WooCommerce brand for '{brand.name}'")
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'name': brand.name,
            })
    except Exception as e:
        return handle_exception(e)

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

@api.get("/brand/", response=List[ItemBrandOut], tags=["Brand"])
def list_all_brand(request):
    brand = ItemBrand.objects.values('name', 'woocommerce_id')
    return list(brand)

@api.get("/brand/{brand_id}/", response=ItemBrandIn, tags=["Brand"])
def read_brand(request, brand_id: int):
    brand = get_object_or_404(ItemBrand, id=brand_id)
    return ItemBrandIn(
        name=brand.name,
        woocommerce_id=brand.woocommerce_id
    )

#Specs:

@api.post("/specs/", response=SpecsIn, tags=["Specs"])
def create_specs(request,payload: SpecsIn):
    try:
        specs = Specs.objects.create(
            description=payload.description,
        )
        try:
            woocommerce_specs_id=create_woocommerce_attrubites(specs.description,specs.description.lower().replace(' ', '-'))
            if woocommerce_specs_id:
                specs.woocommerce_id = woocommerce_specs_id
                specs.save()
                print(f"Created WooCommerce specs '{specs.description}' with ID {woocommerce_specs_id}")
            else:
                print(f"Failed to create WooCommerce specs for '{specs.description}'")
        except Exception as e :
            return JsonResponse({
                'error': f"Error syncing with WooCommerce: {str(e)}"
                }, status=500)
        return JsonResponse({
            'description': specs.description,
            'woo_id' : specs.woocommerce_id,
            
            })
    except Exception as e:
        return handle_exception(e)

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

@api.get("/specs/", response=List[SpecsIn], tags=["Specs"])
def list_all_specs(request):
    specs = Specs.objects.values('description', 'woocommerce_id')
    return list(specs)

@api.get("/specs/{specs_id}/", response=SpecsIn, tags=["Specs"])
def read_specs(request, specs_id: int):
    specs = get_object_or_404(Specs, id=specs_id)
    return SpecsIn(
        description=specs.description,
        woocommerce_id=specs.woocommerce_id
    )

#Unitmeasurments :

@api.post("/unitmeasurments/", response=UnitOfMeasurementIn, tags=["Unitmeasurments"])
def create_unitmeasurments(request,payload: UnitOfMeasurementIn):
    try:
        unitmeasurments = UnitOfMeasurment.objects.create(
                name=payload.name,
                code=payload.code,
                type=payload.type
        )
        try:
            woocommerce_unitmeasurments_id=create_woocommerce_attrubites(unitmeasurments.name,unitmeasurments.name.lower().replace(' ', '-'))
            if woocommerce_unitmeasurments_id:
                unitmeasurments.woocommerce_id = woocommerce_unitmeasurments_id
                unitmeasurments.save()
                print(f"Created WooCommerce unitmeasurments '{unitmeasurments.name}' with ID {woocommerce_unitmeasurments_id}")
            else:
                print(f"Failed to create WooCommerce unitmeasurments for '{unitmeasurments.name}'")
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

@api.get("/unitmeasurments/{unit_id}/", response=UnitOfMeasurementIn, tags=["Unitmeasurments"])
def read_unitmeasurments(request, unit_id: int):
    unit = get_object_or_404(UnitOfMeasurment, id=unit_id)
    return UnitOfMeasurementIn(
        name=unit.name,
        code=unit.code,
        type=unit.type,
        woocommerce_id=unit.woocommerce_id
    )

@api.get("/unit-of-measurement/", response=List[UnitOfMeasurementOut], tags=["Unitmeasurments"])
def list_all_unit_of_measurements(request):
    units = UnitOfMeasurment.objects.all()
    unit_data = [
        {
            "name": unit.name,
            "code": unit.code,
            "type": unit.type,  
            "woocommerce_id": unit.woocommerce_id,
        }
        for unit in units
    ]
    return unit_data

#Tags:

@api.post("/tags/", response=TagsIn, tags=["Tags"])
def create_tags(request,payload: TagsIn):
    try:
        tags = Tags.objects.create(
                name=payload.name,
        )
        try:
            woocommerce_tags_id=create_woocommerce_attrubites(tags.name,tags.name.lower().replace(' ', '-'))
            if woocommerce_tags_id:
                tags.woocommerce_id = woocommerce_tags_id
                tags.save()
                print(f"Created WooCommerce tags '{tags.name}' with ID {woocommerce_tags_id}")
            else:
                print(f"Failed to create WooCommerce tags for '{tags.name}'")
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

@api.delete("/tags/{tags_id}/", response={204: None}, tags=["Tags"])
def delete_tags(request, tags_id: int):
    tags = get_object_or_404(Tags, id=tags_id)
    tags.delete()
    return {"message": "Tags deleted successfully"}

@api.get("/tags/{tags_id}/", response=TagsIn, tags=["Tags"])
def read_tags(request, tags_id: int):
    tags = get_object_or_404(Tags, id=tags_id)
    return TagsIn(
        name=tags.name,
        woocommerce_id=tags.woocommerce_id
    )

@api.get("/tags/", response=List[TagsIn], tags=["Tags"])
def list_all_tags(request):
    tags = Tags.objects.values('name', 'woocommerce_id')
    return list(tags)

#Variations:

@api.post("/VariationsHeader/", response=VariationsHeaderIn, tags=["VariationsHeader"])
def create_VariationsHeader(request,payload: VariationsHeaderIn):
    try:
        VariationsHeaderr = VariationsHeader.objects.create(
        attribute=payload.attribute,
        )
        try:
            woocommerce_VariationsHeaderr_id=create_woocommerce_attrubites(VariationsHeaderr.attribute,VariationsHeaderr.attribute.lower().replace(' ', '-'))
            if woocommerce_VariationsHeaderr_id:
                VariationsHeaderr.woocommerce_id = woocommerce_VariationsHeaderr_id
                VariationsHeaderr.save()
                print(f"Created WooCommerce VariationsHeaderr '{VariationsHeaderr.attribute}' with ID {woocommerce_VariationsHeaderr_id}")
            else:
                print(f"Failed to create WooCommerce VariationsHeaderr for '{VariationsHeaderr.attribute}'")
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
            woocommerce_VariationsDetaill_id=create_woocommerce_attrubites(VariationsDetaill.value,VariationsDetaill.value.lower().replace(' ', '-'))
            if woocommerce_VariationsDetaill_id:
                VariationsDetaill.woocommerce_id = woocommerce_VariationsDetaill_id
                VariationsDetaill.save()
                print(f"Created WooCommerce VariationsDetaill '{VariationsDetaill.value}' with ID {woocommerce_VariationsDetaill_id}")
            else:
                print(f"Failed to create WooCommerce VariationsDetaill for '{VariationsDetaill.value}'")
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

@api.get("/variations-header/", response=List[VariationsHeaderOut], tags=["VariationsHeader"])
def list_all_variations_headers(request):
    headers = VariationsHeader.objects.all()
    header_data = [
        {
            "attribute": header.attribute,
            "woocommerce_id": header.woocommerce_id,
        }
        for header in headers
    ]
    return header_data

@api.get("/variations-detail/", response=List[VariationsDetailOut], tags=["VariationsDetail"])
def list_all_variations_details(request):
    details = VariationsDetail.objects.all()
    detail_data = [
        {
            "variation_id": detail.variation_id,
            "value": detail.value,
            "woocommerce_id": detail.woocommerce_id,
        }
        for detail in details
    ]
    return detail_data

#Item :

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

#Package:

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

@api.delete("/packages/{package_id}/", tags=["Packages"])
def delete_package(request, package_id: int):
    package = Package.objects.get(id=package_id)
    package.delete()
    return {"message": "Package deleted successfully"}

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

@api.get("/packages/", response=List[dict], tags=["Packages"])
def list_packages(request):
    packages = Package.objects.all()
    package_data = [
        {
            "id": package.id,
            "name": package.name,
            "weight": package.weight,
            "length": package.length,
            "height": package.height,
            "width": package.width,
            "material": package.material
        }
        for package in packages
    ]
    return package_data
#Item Packages :

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

@api.delete("/item-packages/{item_package_id}/", tags=["Item Packages"])
def delete_item_package(request, item_package_id: int):
    item_package = ItemPackage.objects.get(id=item_package_id)
    item_package.delete()
    return {"message": "Item Package deleted successfully"}

@api.get("/item-packages/{item_package_id}/", response=ItemPackageIn, tags=["Item Packages"])
def read_item_package(request, item_package_id: int):
    item_package = ItemPackage.objects.get(id=item_package_id)
    return ItemPackageIn(
        item_id=item_package.item.id,
        package_id=item_package.package.id,
        quantity=item_package.quantity,
        barcode=item_package.barcode
    )

@api.get("/item-packages/", response=List[dict], tags=["Item Packages"])
def list_item_packages(request):
    item_packages = ItemPackage.objects.all()
    item_package_data = [
        {
            "item_id": item_package.item_id,
            "package_id": item_package.package_id,
            "quantity": item_package.quantity,
            "barcode": item_package.barcode,
        }
        for item_package in item_packages
    ]
    return item_package_data

#Item Warehouse:

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

@api.delete("/items-warehouses/{items_warehouse_id}/", tags=["Items Warehouses"])
def delete_items_warehouse(request, items_warehouse_id: int):
    items_warehouse = Itemswarehouse.objects.get(id=items_warehouse_id)
    items_warehouse.delete()
    return {"message": "Items Warehouse deleted successfully"}

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

@api.get("/items-warehouse/", response=List[dict], tags=["Items Warehouses"])
def list_items_warehouse(request):
    items_warehouse = Itemswarehouse.objects.all()
    items_warehouse_data = [
        {
            "warehouse_id": item.warehouse_id,
            "item_id": item.item_id,
            "quantity": item.quantity,
            "net_movement": item.net_movement,
            "quantity_reserved": item.quantity_reserved,
            "branch": item.branch,
            "opening": item.opening,
            "opening_quantity": item.opening_quantity,
        }
        for item in items_warehouse
    ]
    return items_warehouse_data

#Integrations : 

@api.post("/integration/", response=IntegrateIn, tags=["Integration"])
def create_integration(request, payload: IntegrateIn):
    try:
        with transaction.atomic():

            integratee = integrate.objects.create(
                type=payload.type,
                consumer_key=payload.consumer_key,
                secret_key=payload.secret_key,
                active=payload.active,
            )


            warehouse_data = payload.warehouse
            warehouse = Warehouse.objects.create(
                name=warehouse_data.name,
                country=warehouse_data.country,
                city=warehouse_data.city,
                address=warehouse_data.address,
                branch=warehouse_data.branch,
                initial_Data=warehouse_data.initial_data,
                default=warehouse_data.default,
                show_room=warehouse_data.show_room,
            )

            return IntegrateIn(
                type=integratee.type,
                consumer_key=integratee.consumer_key,
                secret_key=integratee.secret_key,
                active=integratee.active,
                warehouse=WarehouseIn(
                    name=warehouse.name,
                    country=warehouse.country,
                    city=warehouse.city,
                    address=warehouse.address,
                    branch=warehouse.branch,
                    initial_data=warehouse.initial_Data,
                    default=warehouse.default,
                    show_room=warehouse.show_room
                )
            )
    except Exception as e:
        print(type(e))
        return handle_exception(e)

@api.delete("/integration/{integration_id}/", tags=["Integration"])
def delete_integration(request, integration_id: int):
    try:
        with transaction.atomic():
            integratee = get_object_or_404(integrate, id=integration_id)
            Warehouse.objects.filter(integrate=integratee).delete()
            integratee.delete()
            return {"success": True}
    except Exception as e:
        print(type(e))
        return handle_exception(e)


@api.put("/integration/{integration_id}/", response=IntegrateOut, tags=["Integration"])
def update_integration(request, integration_id: int, payload: IntegrateIn):
    try:
        with transaction.atomic():
            integratee = get_object_or_404(integrate, id=integration_id)

          
            integratee.type = payload.type
            integratee.consumer_key = payload.consumer_key
            integratee.secret_key = payload.secret_key
            integratee.active = payload.active
            integratee.save()


            if payload.warehouse:
                warehouse_data = payload.warehouse


                warehouse, created = Warehouse.objects.get_or_create(
                    integrate=integratee,
                    defaults={
                        'name': warehouse_data.name,
                        'country': warehouse_data.country,
                        'city': warehouse_data.city,
                        'address': warehouse_data.address,
                        'branch': warehouse_data.branch,
                        'initial_Data': warehouse_data.initial_data,
                        'default': warehouse_data.default,
                        'show_room': warehouse_data.show_room,
                    }
                )


                if not created:
                    warehouse.name = warehouse_data.name
                    warehouse.country = warehouse_data.country
                    warehouse.city = warehouse_data.city
                    warehouse.address = warehouse_data.address
                    warehouse.branch = warehouse_data.branch
                    warehouse.initial_Data = warehouse_data.initial_data
                    warehouse.default = warehouse_data.default
                    warehouse.show_room = warehouse_data.show_room
                    warehouse.save()


            updated_integration = integrate.objects.get(id=integratee.id)


            return IntegrateOut(
                id=updated_integration.id,
                type=updated_integration.type,
                consumer_key=updated_integration.consumer_key,
                secret_key=updated_integration.secret_key,
                active=updated_integration.active,
                warehouse=WarehouseIn(
                    name=warehouse.name,
                    country=warehouse.country,
                    city=warehouse.city,
                    address=warehouse.address,
                    branch=warehouse.branch,
                    initial_data=warehouse.initial_Data,
                    default=warehouse.default,
                    show_room=warehouse.show_room
                ) if warehouse else None  
            )

    except Exception as e:
        print(type(e))
        return handle_exception(e)

@api.get("/integration/{integration_id}/", response=IntegrateOut, tags=["Integration"])
def read_integration(request, integration_id: int):
    try:
        integratee = get_object_or_404(integrate, id=integration_id)

   
        warehouse = Warehouse.objects.filter(integrate=integratee).first()


        return IntegrateOut(
            id=integratee.id,
            type=integratee.type,
            consumer_key=integratee.consumer_key,
            secret_key=integratee.secret_key,
            active=integratee.active,
            warehouse=WarehouseIn(
                name=warehouse.name,
                country=warehouse.country,
                city=warehouse.city,
                address=warehouse.address,
                branch=warehouse.branch,
                initial_data=warehouse.initial_Data,
                default=warehouse.default,
                show_room=warehouse.show_room
            ) if warehouse else None  
        )

    except Exception as e:
        print(type(e))
        return handle_exception(e)

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

@api.get("/integrations/", response=List[IntegrateOutt], tags=["Integration"])
def list_integrations(request):
    integrations = integrate.objects.all()
    response = []

    for integratee in integrations:
        try:
            warehouse = Warehouse.objects.get(integrate_id=integratee.id) 
            warehouse_data = WarehouseOut(
                id=warehouse.id,
                name=warehouse.name,
                country=warehouse.country,
                city=warehouse.city,
                address=warehouse.address,
                branch=warehouse.branch,
                initial_data=warehouse.initial_Data,
                default=warehouse.default,
                show_room=warehouse.show_room
            )
        except Warehouse.DoesNotExist:
            warehouse_data = None

        response.append(
            IntegrateOutt(
                id=integratee.id,
                type=integratee.type,
                consumer_key=integratee.consumer_key,
                secret_key=integratee.secret_key,
                active=integratee.active,
                warehouse=warehouse_data
            )
        )

    return response

#warehouse : 

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

@api.get("/warehouses/", response=List[dict], tags=["Warehouses"])
def list_warehouses(request):
    warehouses = Warehouse.objects.all()
    warehouse_data = [
        {
            "id": warehouse.id,
            "name": warehouse.name,
            "country": warehouse.country,
            "city": warehouse.city,
            "address": warehouse.address,
            "branch": warehouse.branch,
            "initial_data": warehouse.initial_Data,
            "default": warehouse.default,
            "show_room": warehouse.show_room,
        }
        for warehouse in warehouses
    ]
    return warehouse_data


#Billing address:
@api.post("/billing/",response=BillingAddressIn,tags=["Billing address"])
def create_billing_address(request , payload:BillingAddressIn):
    try:
            billing=BillingAddress.objects.create(
                first_name=payload.first_name,
                last_name=payload.last_name,
                company=payload.company,
                address_1=payload.address_1,
                address_2=payload.address_2,
                state=payload.state,
                postcode=payload.postcode,
                phone=payload.phone,
                email=payload.email,
                country=payload.country,
                city=payload.city,
            )
            return BillingAddressIn(
                first_name=billing.first_name,
                last_name=billing.last_name,
                company=billing.company,
                address_1=billing.address_1,
                address_2=billing.address_2,
                state=billing.state,
                city=billing.city,
                postcode=billing.postcode,
                phone=billing.phone,
                email=billing.email,
                country=billing.country,
            )
    except Exception as e:
        return handle_exception(e)

@api.put("/billing/{billing_id}/", response=BillingAddressIn, tags=["Billing address"])
def update_billing(request, billing_id: int, payload: BillingAddressIn):
    billing = get_object_or_404(BillingAddress, id=billing_id)
    for attr, value in payload.dict().items():
        setattr(billing, attr, value)
    billing.save()
    return BillingAddressIn(
        first_name=billing.first_name,
        last_name=billing.last_name,
        company=billing.company,
        address_1=billing.address_1,
        address_2=billing.address_2,
        state=billing.state,
        city=billing.city,
        postcode=billing.postcode,
        phone=billing.phone,
        email=billing.email,
        country=billing.country,
    )

@api.delete("/billing/{billing_id}/", response={204: None}, tags=["Billing address"])
def delete_billing(request, billing_id: int):
    billing = get_object_or_404(BillingAddress, id=billing_id)
    billing.delete()
    return {"message": "Billing deleted successfully"}

@api.get("/billing/{billing_id}/", response=BillingAddressIn, tags=["Billing address"])
def read_billing(request, billing_id: int):
    billing = get_object_or_404(BillingAddress, id=billing_id)
    return BillingAddressIn(
        first_name=billing.first_name,
        last_name=billing.last_name,
        company=billing.company,
        address_1=billing.address_1,
        address_2=billing.address_2,
        state=billing.state,
        city=billing.city,
        postcode=billing.postcode,
        phone=billing.phone,
        email=billing.email,
        country=billing.country,
    )

#Shipping Address :

@api.post("/shipping/",response=ShippingAddressIn,tags=["Shipping Address"])
def create_shipping_address(request , payload:ShippingAddressIn):
    try:
            shipping=ShippingAddress.objects.create(
                first_name=payload.first_name,
                last_name=payload.last_name,
                company=payload.company,
                address_1=payload.address_1,
                address_2=payload.address_2,
                state=payload.state,
                postcode=payload.postcode,
                country=payload.country,
                city=payload.city,
            )
            return ShippingAddressIn(
                first_name=shipping.first_name,
                last_name=shipping.last_name,
                company=shipping.company,
                address_1=shipping.address_1,
                address_2=shipping.address_2,
                state=shipping.state,
                city=shipping.city,
                postcode=shipping.postcode,
                country=shipping.country,
            )
    except Exception as e:
        return handle_exception(e)

@api.put("/shipping/{shipping_id}/", response=ShippingAddressIn, tags=["Shipping Address"])
def update_shipping(request, shipping_id: int, payload: ShippingAddressIn):
    shipping = get_object_or_404(ShippingAddress, id=shipping_id)
    for attr, value in payload.dict().items():
        setattr(shipping, attr, value)
    shipping.save()
    return ShippingAddressIn(
                first_name=shipping.first_name,
                last_name=shipping.last_name,
                company=shipping.company,
                address_1=shipping.address_1,
                address_2=shipping.address_2,
                state=shipping.state,
                city=shipping.city,
                postcode=shipping.postcode,
                country=shipping.country,
            )

@api.delete("/shipping/{shipping_id}/", response={204: None}, tags=["Shipping Address"])
def delete_billing(request, shipping_id: int):
    shipping = get_object_or_404(ShippingAddress, id=shipping_id)
    shipping.delete()
    return {"message": "Shipping deleted successfully"}

@api.get("/shipping/{shipping_id}/", response=ShippingAddressIn, tags=["Shipping Address"])
def read_shipping(request, shipping_id: int):
    shipping = get_object_or_404(ShippingAddress, id=shipping_id)
    return ShippingAddressIn(
                first_name=shipping.first_name,
                last_name=shipping.last_name,
                company=shipping.company,
                address_1=shipping.address_1,
                address_2=shipping.address_2,
                state=shipping.state,
                city=shipping.city,
                postcode=shipping.postcode,
                country=shipping.country,
            )

#Customer:

@api.post("/customers/", response=CustomerIn, tags=["Customers"])
def create_customer(request, payload: CustomerIn):
    try:
        with transaction.atomic():
            billing_address = BillingAddress.objects.get(id=payload.customerbiling_id)
            
            shipping_address = ShippingAddress.objects.get(id=payload.customershipping_id)

            customer = Customer.objects.create(
                email=payload.email,
                first_name=payload.first_name,
                last_name=payload.last_name,
                role=payload.role,
                username=payload.username,
                password=payload.password,
                is_paying_customer=payload.is_paying_customer,
                avatar_url=payload.avatar_url,
                customerbiling_id=billing_address,
                customershipping_id=shipping_address
            )
            woocommerce_id = create_woocommerce_customer(customer.first_name, customer.email)
            if woocommerce_id:
                customer.woocommerce_id = woocommerce_id
                customer.save(update_fields=['woocommerce_id'])  

            logger.info(f"Successfully created WooCommerce customer '{customer.email}' with ID {woocommerce_id}")
            return JsonResponse({
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'role': customer.role,
                    'username': customer.username,
                    'is_paying_customer': customer.is_paying_customer,
                    'avatar_url': customer.avatar_url,
                    'customerbiling_id': customer.customerbiling_id.id,
                    'customershipping_id': customer.customershipping_id.id,
                    'woocommerce_id': customer.woocommerce_id,
                    }, status=201)
    except Exception as e:
        return JsonResponse({
            'error': f"Error creating customer: {str(e)}"
        }, status=500)
    
@api.get("/customers/{customer_id}/", response=CustomerOut, tags=["Customers"])
def read_customer(request, customer_id: int):
    try:
        customer = Customer.objects.get(id=customer_id)
        return JsonResponse({
            'id': customer.id,
            'email': customer.email,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'role': customer.role,
            'username': customer.username,
            'is_paying_customer': customer.is_paying_customer,
            'avatar_url': customer.avatar_url,
            'customer_billing_id': customer.customerbiling_id.id if customer.customerbiling_id else None,
            'customer_shipping_id': customer.customershipping_id.id if customer.customershipping_id else None,
            'woocommerce_id': customer.woocommerce_id,
        })
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api.get("/customers/", response=List[CustomerOut], tags=["Customers"])
def list_customers(request):
    try:
        customers = Customer.objects.all()
        customer_list = []
        for customer in customers:
            customer_list.append({
                'id': customer.id,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'role': customer.role,
                'username': customer.username,
                'is_paying_customer': customer.is_paying_customer,
                'avatar_url': customer.avatar_url,
            'customer_billing_id': customer.customerbiling_id.id if customer.customerbiling_id else None,
            'customer_shipping_id': customer.customershipping_id.id if customer.customershipping_id else None,
                'woocommerce_id': customer.woocommerce_id,
            })
        return JsonResponse(customer_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api.put("/customers/{customer_id}/", response=CustomerOut, tags=["Customers"])
def update_customer(request, customer_id: int, payload: CustomerIn):
    try:
        customer = Customer.objects.get(id=customer_id)

        customer.email = payload.email
        customer.first_name = payload.first_name
        customer.last_name = payload.last_name
        customer.role = payload.role
        customer.username = payload.username
        customer.password = payload.password
        customer.is_paying_customer = payload.is_paying_customer
        customer.avatar_url = payload.avatar_url
        
        if payload.customerbiling_id:
            billing_address = BillingAddress.objects.get(id=payload.customerbiling_id)
            customer.customerbiling_id = billing_address


        if payload.customershipping_id:
            shipping_address = ShippingAddress.objects.get(id=payload.customershipping_id)
            customer.customershipping_id = shipping_address

        customer.save()

        if customer.woocommerce_id:
            success = update_woocommerce_customer(customer.woocommerce_id, payload.first_name ,payload.email)
            if success:
                print(f"Successfully updated WooCommerce customer '{customer.email}'")
            else:
                print(f"Failed to update WooCommerce customer '{customer.email}'")

        return CustomerOut(
            id=customer.id,
            email=customer.email,
            first_name=customer.first_name,
            last_name=customer.last_name,
            role=customer.role,
            username=customer.username,
            is_paying_customer=customer.is_paying_customer,
            avatar_url=customer.avatar_url,
            customerbiling_id=customer.customerbiling_id.id if customer.customerbiling_id else None,
            customershipping_id=customer.customershipping_id.id if customer.customershipping_id else None,
            woocommerce_id=customer.woocommerce_id,
        )
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except BillingAddress.DoesNotExist:
        return JsonResponse({'error': 'Billing Address not found'}, status=404)
    except ShippingAddress.DoesNotExist:
        return JsonResponse({'error': 'Shipping Address not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api.get("/customers/{first_name}/{last_name}/", response=CustomerOut, tags=["Customers"])
def search_customer_by_name(request, first_name: str, last_name: str):
    try:
        customers = Customer.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
        
        if not customers.exists():
            return JsonResponse({'error': 'No customers found matching the provided criteria'}, status=404)
        
        customer_data = []
        for customer in customers:
            customer_data.append({
                'id': customer.id,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'role': customer.role,
                'username': customer.username,
                'is_paying_customer': customer.is_paying_customer,
                'avatar_url': customer.avatar_url,
                'customer_billing_id': customer.customerbiling_id.id if customer.customerbiling_id else None,
                'customer_shipping_id': customer.customershipping_id.id if customer.customershipping_id else None,
                'woocommerce_id': customer.woocommerce_id,
            })
        
        return JsonResponse(customer_data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api.delete("/customers/{customer_id}/", tags=["Customers"])
def delete_customer(request, customer_id: int):
    try:
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return JsonResponse({'message': f'Customer with ID {customer_id} deleted successfully'})
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api.put("/customer/change-password", response={200: str},tags=["Customers"])
def change_password(request, username: str,payload:Newpassword):
    customer = get_object_or_404(Customer, username=username)
    customer.password=payload.password
    customer.save()
    return JsonResponse({'message': f'Password changed successfully'})

#Order:

@api.post("/orders/", response=OrderIn, tags=["Orders"])
def create_order(request, payload: OrderIn):
    try:
        with transaction.atomic():
            billing_address = BillingAddress.objects.get(id=payload.customerbiling_id)
            shipping_address = ShippingAddress.objects.get(id=payload.customershipping_id)
            customer = Customer.objects.get(id=payload.customer_id)

            order = Order.objects.create(
                parent_id=payload.parent_id,
                number=payload.number,
                order_key=payload.order_key,
                created_via=payload.created_via,
                version=payload.version,
                status=payload.status,
                currency=payload.currency,
                discount_total=payload.discount_total,
                discount_tax=payload.discount_tax,
                shipping_total=payload.shipping_total,
                shipping_tax=payload.shipping_tax,
                cart_tax=payload.cart_tax,
                total=payload.total,
                total_tax=payload.total_tax,
                prices_include_tax=payload.prices_include_tax,
                payment_method=payload.payment_method,
                date_paid=payload.date_paid,
                date_completed=payload.date_completed,
                cart_hash=payload.cart_hash,
                set_paid=payload.set_paid,
                woocommerce_id=payload.woocommerce_id,
                customer_id=customer,
                customerbiling_id=billing_address,
                customershipping_id=shipping_address,
            )

            
            woocommerce_id = create_woocommerce_order(order.number,order.status,order.total)
            if woocommerce_id:
                order.woocommerce_id = woocommerce_id
                order.save(update_fields=['woocommerce_id'])

            return JsonResponse(payload.dict(), status=201)

    except Exception as e:
        return JsonResponse({"error": f"Error creating order: {str(e)}"}, status=500)
    
@api.put("/orders/{id}/", response=OrderIn, tags=["Orders"])
def update_order(request, id: int, payload: OrderIn):
    try:
        with transaction.atomic():
            order = get_object_or_404(Order, id=id)

            order.parent_id = payload.parent_id
            order.number = payload.number
            order.order_key = payload.order_key
            order.created_via = payload.created_via
            order.version = payload.version
            order.status = payload.status
            order.currency = payload.currency
            order.discount_total = payload.discount_total
            order.discount_tax = payload.discount_tax
            order.shipping_total = payload.shipping_total
            order.shipping_tax = payload.shipping_tax
            order.cart_tax = payload.cart_tax
            order.total = payload.total
            order.total_tax = payload.total_tax
            order.prices_include_tax = payload.prices_include_tax
            order.payment_method = payload.payment_method
            order.date_paid = payload.date_paid
            order.date_completed = payload.date_completed
            order.cart_hash = payload.cart_hash
            order.set_paid = payload.set_paid
            order.woocommerce_id = payload.woocommerce_id
            
            try:
                billing_address = BillingAddress.objects.get(id=payload.customerbiling_id)
                shipping_address = ShippingAddress.objects.get(id=payload.customershipping_id)
                customer = Customer.objects.get(id=payload.customer_id)

                order.customer_id = customer
                order.customerbiling_id = billing_address
                order.customershipping_id = shipping_address

            except Customer.DoesNotExist as e:
                return JsonResponse({"error": f"Customer matching query does not exist: {e}"}, status=404)
            except (BillingAddress.DoesNotExist, ShippingAddress.DoesNotExist) as e:
                return JsonResponse({"error": f"Related address matching query does not exist: {e}"}, status=404)

            order.save()

     
            update_woocommerce_order(order.id, order.number)

            return JsonResponse(payload.dict(), status=200)

    except Exception as e:
        return JsonResponse({"error": f"Error updating order: {str(e)}"}, status=500)

@api.delete("/orders/{id}/", tags=["Orders"])
def delete_order(request, id: int):
    try:
        with transaction.atomic():
            order = get_object_or_404(Order, id=id)

            # Delete from WooCommerce first if WooCommerce ID exists
            if order.woocommerce_id:
                if not delete_woocommerce_order(order.woocommerce_id):
                    return JsonResponse({"error": "Failed to delete order from WooCommerce"}, status=500)

            order.delete()
            return JsonResponse({"message": "Order deleted successfully"}, status=204)

    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Error deleting order: {str(e)}"}, status=500)

@api.get("/orders/{id}/", response=OrderOut, tags=["Orders"])
def read_order(request, id: int):
    try:
        order = Order.objects.get(id=id)
        return OrderOut(
            id=order.id,
            parent_id=order.parent_id,
            number=order.number,
            order_key=order.order_key,
            created_via=order.created_via,
            version=order.version,
            status=order.status,
            currency=order.currency,
            discount_total=order.discount_total,
            discount_tax=order.discount_tax,
            shipping_total=order.shipping_total,
            shipping_tax=order.shipping_tax,
            cart_tax=order.cart_tax,
            total=order.total,
            total_tax=order.total_tax,
            prices_include_tax=order.prices_include_tax,
            payment_method=order.payment_method,
            date_paid=order.date_paid.strftime('%Y-%m-%dT%H:%M:%S') if order.date_paid else None,
            date_completed=order.date_completed.strftime('%Y-%m-%dT%H:%M:%S') if order.date_completed else None,
            cart_hash=order.cart_hash,
            set_paid=order.set_paid,
            woocommerce_id=order.woocommerce_id,
            customer_id=order.customer_id.id if order.customer_id else None,
            customerbiling_id=order.customerbiling_id.id if order.customerbiling_id else None,
            customershipping_id=order.customershipping_id.id if order.customershipping_id else None,
        ).dict()
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api.get("/orders/", response=List[OrderOut], tags=["Orders"])
def list_orders(request):
    orders = Order.objects.all()
    order_list=[]
    for order in orders:
        order_list.append(OrderOut(
            id=order.id,
            parent_id=order.parent_id,
            number=order.number,
            order_key=order.order_key,
            created_via=order.created_via,
            version=order.version,
            status=order.status,
            currency=order.currency,
            discount_total=order.discount_total,
            discount_tax=order.discount_tax,
            shipping_total=order.shipping_total,
            shipping_tax=order.shipping_tax,
            cart_tax=order.cart_tax,
            total=order.total,
            total_tax=order.total_tax,
            prices_include_tax=order.prices_include_tax,
            payment_method=order.payment_method,
            date_paid=order.date_paid.strftime('%Y-%m-%dT%H:%M:%S')
            if order.date_paid else None,
            date_completed=order.date_completed.strftime('%Y-%m-%dT%H:%M:%S')
            if order.date_completed else None,
            cart_hash=order.cart_hash,
            set_paid=order.set_paid,
            woocommerce_id=order.woocommerce_id,
            customer_id=order.customer_id.id if order.customer_id else None,
            customerbiling_id=order.customerbiling_id.id if order.customerbiling_id else None,
            customershipping_id=order.customershipping_id.id if order.customershipping_id else None,
            ).dict())
        return JsonResponse(order_list, safe=False)
    
@api.get("/order/{order_number}", response=OrderOut, tags=["Orders"])
def search_order_by_number(request, order_number: str):
    order = get_object_or_404(Order, number=order_number)
    
    order_data = {
        'id': order.id,
        'parent_id': order.parent_id,
        'number': order.number,
        'order_key': order.order_key,
        'created_via': order.created_via,
        'version': order.version,
        'status': order.status,
        'currency': order.currency,
        'discount_total': order.discount_total,
        'discount_tax': order.discount_tax,
        'shipping_total': order.shipping_total,
        'shipping_tax': order.shipping_tax,
        'cart_tax': order.cart_tax,
        'total': order.total,
        'total_tax': order.total_tax,
        'prices_include_tax': order.prices_include_tax,
        'payment_method': order.payment_method,
        'date_paid': convert_datetime_to_string(order.date_paid),
        'date_completed': convert_datetime_to_string(order.date_completed),
        'cart_hash': order.cart_hash,
        'set_paid': order.set_paid,
        'woocommerce_id': order.woocommerce_id,
        'customer_id': order.customer_id.id,
        'customerbiling_id': order.customerbiling_id.id,
        'customershipping_id': order.customershipping_id.id
    }
    
    return OrderOut(**order_data)

@api.get("/customer/{customer_id}/orders", response=List[OrderOut], tags=["Orders"])
def get_customer_order_history(request, customer_id: int):
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer_id=customer.id)
    
    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'parent_id': order.parent_id,
            'number': order.number,
            'order_key': order.order_key,
            'created_via': order.created_via,
            'version': order.version,
            'status': order.status,
            'currency': order.currency,
            'discount_total': order.discount_total,
            'discount_tax': order.discount_tax,
            'shipping_total': order.shipping_total,
            'shipping_tax': order.shipping_tax,
            'cart_tax': order.cart_tax,
            'total': order.total,
            'total_tax': order.total_tax,
            'prices_include_tax': order.prices_include_tax,
            'payment_method': order.payment_method,
            'date_paid': convert_datetime_to_string(order.date_paid),
            'date_completed': convert_datetime_to_string(order.date_completed),
            'cart_hash': order.cart_hash,
            'set_paid': order.set_paid,
            'woocommerce_id': order.woocommerce_id,
            'customer_id': order.customer_id.id,
            'customerbiling_id': order.customerbiling_id.id,
            'customershipping_id': order.customershipping_id.id
        }
        order_list.append(OrderOut(**order_data))
    
    return order_list

def get_order_statuses_by_customer(customer_id: int) -> List[dict[str, str]]:
    orders = Order.objects.filter(customer_id=customer_id)
    statuses = [{"status": order.status} for order in orders]
    return statuses

@api.get("/orders/status/{customer_id}", response=List[dict[str, str]], tags=["Orders"])
def order_statuses(request, customer_id: int):
    statuses = get_order_statuses_by_customer(customer_id)
    return statuses