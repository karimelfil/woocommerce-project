import os
import django
import requests
from requests.auth import HTTPBasicAuth


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
django.setup()

from ecommerce.models import Tags


consumer_key = 'ck_b905c5395fbfee15c4683104e148918bb31f1739'
consumer_secret = 'cs_a31a9e81dface34df2e367fb45b45ef39f0fa81b'
store_url = 'https://eldrapaints.com/wp-json/wc/v3/products/tags'



def create_woocommerce_tags(name, slug):
    data = {
        'name': name,
        'slug': slug
    }

    response = requests.post(store_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)

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
            print(f"Created WooCommerce tag '{tag.name}' with ID {woocommerce_tag_id}")

if __name__ == "__main__":
    sync_tags()


