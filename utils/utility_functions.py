import os
import json
import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from urllib.parse import urlparse
import matplotlib.pyplot as plt


def fetch_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def draw_polygon_on_image(image, polygon_points):
    draw = ImageDraw.Draw(image)
    polygon = [(point['x'], point['y']) for point in eval(polygon_points)]
    draw.polygon(polygon, outline="red")
    return image


def visualize_random_rows(data, n=3):
    samples = data.sample(n)
    fig, axes = plt.subplots(1, n, figsize=(15, 5))
    
    for i, (_, row) in enumerate(samples.iterrows()):
        img = fetch_image(row['2D Image URL'])
        img = draw_polygon_on_image(img, row['2D Image Points'])
        axes[i].imshow(img)
        axes[i].set_title(f"Name: {row['Name']}\nGroup: {row['Group Name']}\nLabel: {row['Label']}")
        axes[i].axis('off')


def visualize_random_rows_updated(data, n=3):
    samples = data.sample(n)
    fig, axes = plt.subplots(1, n, figsize=(15, 5))
    
    for i, (_, row) in enumerate(samples.iterrows()):
        img = fetch_image(row['2D Image URL'])
        img = draw_polygon_on_image(img, row['2D Image Points'])
        axes[i].imshow(img)
        axes[i].set_title(f"File Name: {row['Image File Name']}\nGroup: {row['Group Name']}\nLabel: {row['Label']}")
        axes[i].axis('off')

# Function to convert polygon to bounding box
def polygon_to_bbox(polygon):
    x_coords = [point['x'] for point in polygon]
    y_coords = [point['y'] for point in polygon]
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    width = max_x - min_x
    height = max_y - min_y
    return {
        "left": min_x,
        "top": min_y,
        "width": width,
        "height": height
    }


def draw_bboxes_on_image(image, bbox_list):
    """
    Draw bounding boxes on an image.

    Parameters:
    - image: PIL Image object
    - bbox_list: List of bounding box coordinates (x_min, y_min, x_max, y_max)

    Returns:
    - image: PIL Image object with bounding boxes drawn
    """
    draw = ImageDraw.Draw(image)
    for bbox in bbox_list:
        x_min, y_min, x_max, y_max = bbox
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
    return image


def visualize_images_with_bboxes_from_roboflow(json_file, n=3):
    """
    Visualizes random images with bounding boxes from a Roboflow format JSON dataset.

    Parameters:
    - json_file: Path to the Roboflow JSON dataset file
    - n: Number of random samples to visualize (default: 3)

    Displays:
    - Subplots of images with bounding boxes drawn
    """
    with open(json_file, 'r') as f:
        dataset = json.load(f)
    
    samples = random.sample(dataset['annotations'], n)  # Assuming annotations contain bbox info
    fig, axes = plt.subplots(1, n, figsize=(15, 5))
    
    for i, annotation in enumerate(samples):
        image_url = annotation['image']
        bbox_list = annotation['annotations']  # Assuming 'annotations' contains bbox info
        
        # Fetch image from URL
        img = fetch_image(image_url)
        
        # Draw bounding boxes on the image
        img_with_bbox = draw_bboxes_on_image(img.copy(), bbox_list)
        
        # Display the image with bounding boxes
        axes[i].imshow(img_with_bbox)
        axes[i].set_title(f"Image: {image_url}")
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()


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

import matplotlib.patches as patches
from PIL import Image, UnidentifiedImageError

# Function to plot a single image with its annotations
def plot_image_with_polygon_annotations(ax, image_data):
    image_url = image_data['image_urls'][0]  # Use the first URL for simplicity
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        img = Image.open(BytesIO(response.content))

        ax.imshow(img)
        labels = []
        for annotation in image_data['annotations']:
            points = annotation['points']
            # Convert points to a list of tuples
            polygon_points = [(point['x'], point['y']) for point in points]
            # Ensure points are valid (each point should be a tuple of two values)
            if all(isinstance(point, tuple) and len(point) == 2 for point in polygon_points):
                polygon = patches.Polygon(polygon_points, closed=True, edgecolor='r', facecolor='none', linewidth=2)
                ax.add_patch(polygon)
                labels.append(annotation['label'])
            else:
                print(f"Invalid points for annotation: {annotation}")

        ax.axis('off')
        image_file_name = image_data['image_file_name']
        return ', '.join(set(labels)), image_file_name  # Return labels and image file name

    except (requests.RequestException, UnidentifiedImageError) as e:
        print(f"Error loading image from {image_url}: {e}")
        return '', ''

# Function to plot multiple images side by side
def visualize_random_images_with_polygon_annotations(combined_annotations, num_images_to_visualize):
    # Select a random subset of images to visualize
    random_images = random.sample(combined_annotations, num_images_to_visualize)

    # Plot the selected images with annotations
    fig, axs = plt.subplots(1, num_images_to_visualize, figsize=(5 * num_images_to_visualize, 5))

    all_labels = []
    all_image_names = []
    for ax, image_data in zip(axs, random_images):
        labels, image_name = plot_image_with_polygon_annotations(ax, image_data)
        all_labels.append(labels)
        all_image_names.append(image_name)

    # Add labels and image file names at the bottom of each subplot
    for ax, labels, image_name in zip(axs, all_labels, all_image_names):
        ax.set_title(labels, fontsize=12, color='black', backgroundcolor='white')
        ax.text(0.5, -0.1, image_name, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10)

    plt.tight_layout()
    plt.show()

# Function to plot a single image with its annotations
def plot_image_with_bbox_annotations(ax, image_data):
    image_url = image_data['image_urls'][0]  # Use the first URL for simplicity
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        img = Image.open(BytesIO(response.content))

        ax.imshow(img)
        labels = []
        for annotation in image_data['annotations']:
            label = annotation['label']
            bbox = annotation['bbox']
            rect = plt.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            labels.append(annotation['label'])
            
        ax.axis('off')
        image_file_name = image_data['image_file_name']
        return ', '.join(set(labels)), image_file_name  # Return labels and image file name

    except (requests.RequestException, UnidentifiedImageError) as e:
        print(f"Error loading image from {image_url}: {e}")
        return '', ''

# Function to plot multiple images side by side
def visualize_random_images_with_bbox_annotations(combined_annotations, num_images_to_visualize):
    # Select a random subset of images to visualize
    random_images = random.sample(combined_annotations, num_images_to_visualize)

    # Plot the selected images with annotations
    fig, axs = plt.subplots(1, num_images_to_visualize, figsize=(5 * num_images_to_visualize, 5))

    all_labels = []
    all_image_names = []
    for ax, image_data in zip(axs, random_images):
        labels, image_name = plot_image_with_bbox_annotations(ax, image_data)
        all_labels.append(labels)
        all_image_names.append(image_name)

    # Add labels and image file names at the bottom of each subplot
    for ax, labels, image_name in zip(axs, all_labels, all_image_names):
        ax.set_title(labels, fontsize=12, color='black', backgroundcolor='white')
        ax.text(0.5, -0.1, image_name, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10)

    plt.tight_layout()
    plt.show()
