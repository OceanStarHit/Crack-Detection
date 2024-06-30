import json
import random
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from network_functions import fetch_image


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

# Function to plot a single image with its annotations
def plot_image_with_polygon_annotations(ax, image_data):
    image_url = image_data['image_urls'][0]  # Use the first URL for simplicity
    img = fetch_image(image_url)
    
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
    img = fetch_image(image_url)


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
