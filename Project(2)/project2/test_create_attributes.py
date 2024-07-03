import os
import django
import requests
from requests.auth import HTTPBasicAuth
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
django.setup()

from ecommerce.models import  UnitOfMeasurment, VariationsDetail , VariationsHeader

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



def sync_variationheader():
    attributes = VariationsHeader.objects.all()

    for attribute in attributes:
        woocommerce_attrubites_id = create_woocommerce_attrubites(attribute.attribute, attribute.attribute.lower().replace(' ', '-'))
        if woocommerce_attrubites_id:
            attribute.woocommerce_id=woocommerce_attrubites_id
            attribute.save()
            print(f"Created WooCommerce VariationsHeader '{attribute.attribute}' with ID {woocommerce_attrubites_id}")



if __name__ == "__main__":
    sync_unit()
    sync_variationsdetail()
    sync_variationheader()





