import os
import requests
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse
from PIL import Image, UnidentifiedImageError


def fetch_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        img = Image.open(BytesIO(response.content))
        return img
    except (requests.RequestException, UnidentifiedImageError) as e:
        print(f"Error loading image from {image_url}: {e}")
        return '', ''

# Function to get the final redirected URL
def get_final_url(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# Function to extract the image name from the URL
def get_image_name(url):
    parsed_url = urlparse(url)
    # Get the last segment of the path (which is the file name)
    image_name = os.path.basename(parsed_url.path)
    return image_name


