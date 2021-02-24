# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_mediumapi.ipynb (unless otherwise specified).

__all__ = ['base_request', 'auth_header', 'fetch_user_data', 'get_user_id', 'fetch_publications', 'post_article',
           'post_image']

# Cell
from requests import get, post, HTTPError
import os

# Cell
def base_request():
    try:
        response = get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Successfull GET Request')

# Cell
def auth_header(token = None, test = False):
    if token is None:
        token = os.getenv('MEDIUM_TOKEN') if not test else os.getenv('MEDIUM_TOKEN_TEST')
    return {'Authorization': f"Bearer {token}"}

# Cell
def fetch_user_data(test = False):
    return get("https://api.medium.com/v1/me", headers = auth_header(test = test))

# Cell
def get_user_id(test = False):
    return fetch_user_data(test).json()['data']['id']

# Cell
def fetch_publications():
    return get(f"https://api.medium.com/v1/users/{get_user_id()}/publications", headers = auth_header())

# Cell
def post_article(
    title,
    content,
    contentFormat = 'markdown',
    tags = None,
    canonicalUrl = None,
    publishStatus = 'draft',
    license = None,
    notifyFollowers = False,
    test = False # internal
):
    data = {
        'title': title,
        'contentFormat': contentFormat,
        'content': content,
        'tags': tags,
        'canonicalUrl': canonicalUrl,
        'publishStatus': publishStatus,
        'license': license,
        'notifyFollowers': notifyFollowers
    }

    return post(f"https://api.medium.com/v1/users/{get_user_id(test)}/posts",
                data = data,
                headers = auth_header(test = test))

# Cell
import random
from io import BytesIO

def post_image(filename = None, img = None, test = False):
    """
    filename: needs to be a valid image file path supported my Medium
    img: can be a binary image representation
    """
    if img is None:
        img = open(filename, 'rb')
    else:
        filename = str(random.randint(1e4, 1e5))
    files = {
        'image': (os.path.basename(filename), img, 'image/png')
    }
    img.close() if img is None else 1
    return post(f"https://api.medium.com/v1/images",
                headers = auth_header(test = test),
                files = files)