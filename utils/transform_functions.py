

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


def points_to_bbox(points):
    x_coords = [point['x'] for point in points]
    y_coords = [point['y'] for point in points]
    x_min = min(x_coords)
    y_min = min(y_coords)
    width = max(x_coords) - x_min
    height = max(y_coords) - y_min
    return [x_min, y_min, width, height]


def xywh_to_xyxy(xywh):
    x, y, w, h = xywh
    x2 = x + w
    y2 = y + h
    xyxy = [x, y, x2, y2]
    return xyxy


def xyxy_to_xywh(xyxy):
    x, y, x2, y2 = xyxy
    w = x2 - x
    h = y2 - y
    xywh = [x, y, w, h]
    return xywh


def convert_ground_truths(ground_truths):
    images_ground_truths = []

    for ground_truth in ground_truths:
        image_gt = []
        boxes = ground_truth['boxes']
        labels = ground_truth['labels']

        for i in range(len(labels)):
            label = int(labels[i])  # Convert label to integer
            box = boxes[i].tolist()  # Convert numpy array to list
            xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
            width = xmax - xmin
            height = ymax - ymin
            bounding_box = [xmin, ymin, width, height]

            image_gt.append({'label': label, 'bounding_box': bounding_box})

        images_ground_truths.append(image_gt)

    return images_ground_truths


def convert_predictions(predictions):
    images_predictions = []

    for image_pred in predictions:
        image_predictions = []
        boxes = image_pred['boxes']
        labels = image_pred['labels']
        scores = image_pred['scores']

        for i in range(len(labels)):
            label = int(labels[i])  # Convert label to integer
            score = float(scores[i])  # Convert score to float
            box = boxes[i].tolist()  # Convert numpy array to list
            xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
            width = xmax - xmin
            height = ymax - ymin
            bounding_box = [int(xmin), int(ymin), int(width), int(height)]  # Convert to integers

            image_predictions.append({
                'label': label,
                'probability': score,
                'bounding_box': bounding_box
            })

        images_predictions.append(image_predictions)

    return images_predictions

