import numpy as np

import numpy as np

def calculate_precision_recall(predictions, ground_truths, prob_threshold=0.5, overlap_threshold=0.5):
    """
    Calculate Precision and Recall for object detection predictions.

    Args:
    - predictions (list): List of dictionaries containing prediction data.
      Each dictionary should have keys 'label', 'probability', 'bounding_box'.
      Example format:
      [{'label': 'car', 'probability': 0.92, 'bounding_box': [x, y, width, height]}, ...]
      
    - ground_truths (list): List of dictionaries containing ground truth data.
      Each dictionary should have keys 'label' and 'bounding_box'.
      Example format:
      [{'label': 'car', 'bounding_box': [x, y, width, height]}, ...]
      
    - prob_threshold (float): Minimum probability threshold for predictions.
    
    - overlap_threshold (float): Minimum IoU threshold for considering a detection as correct.

    Returns:
    - precision (float): Precision score.
    - recall (float): Recall score.
    """
    # Filter predictions based on probability threshold
    predictions = [pred for pred in predictions if pred['probability'] >= prob_threshold]

    # Initialize variables
    true_positives = 0
    false_positives = len(predictions)
    false_negatives = len(ground_truths)

    for gt in ground_truths:
        found_match = False
        for pred in predictions:
            if pred['label'] == gt['label']:
                iou = calculate_iou(pred['bounding_box'], gt['bounding_box'])
                if iou >= overlap_threshold:
                    found_match = True
                    break

        if found_match:
            true_positives += 1
            false_positives -= 1
            false_negatives -= 1

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    return precision, recall


def calculate_iou(boxA, boxB):
    """
    Calculate Intersection over Union (IoU) of two bounding boxes.

    Args:
    - boxA (list): Coordinates of first bounding box in format [x, y, width, height].
    - boxB (list): Coordinates of second bounding box in format [x, y, width, height].

    Returns:
    - iou (float): Intersection over Union (IoU) score.
    """
    # Convert to (x1, y1, x2, y2) format
    x1A, y1A, wA, hA = boxA[0], boxA[1], boxA[2], boxA[3]
    x1B, y1B, wB, hB = boxB[0], boxB[1], boxB[2], boxB[3]
    x2A, y2A = x1A + wA, y1A + hA
    x2B, y2B = x1B + wB, y1B + hB

    # Calculate intersection area
    xA = max(x1A, x1B)
    yA = max(y1A, y1B)
    xB = min(x2A, x2B)
    yB = min(y2A, y2B)

    inter_area = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # Calculate area of each box
    boxAArea = wA * hA
    boxBArea = wB * hB

    # Calculate union area
    union_area = boxAArea + boxBArea - inter_area

    # Calculate IoU
    iou = inter_area / union_area if union_area > 0 else 0

    return iou


def calculate_map(predictions, ground_truths, prob_threshold=0.5, overlap_threshold=0.5):
    """
    Calculate mean Average Precision (mAP) for object detection.

    Args:
    - predictions (list): List of dictionaries containing prediction data.
      Each dictionary should have keys 'label', 'probability', 'bounding_box'.
      Example format:
      [{'label': 'car', 'probability': 0.92, 'bounding_box': [x, y, width, height]}, ...]
      
    - ground_truths (list): List of dictionaries containing ground truth data.
      Each dictionary should have keys 'label' and 'bounding_box'.
      Example format:
      [{'label': 'car', 'bounding_box': [x, y, width, height]}, ...]
      
    - prob_threshold (float): Minimum probability threshold for predictions.
    
    - overlap_threshold (float): Minimum IoU threshold for considering a detection as correct.

    Returns:
    - mAP (float): mean Average Precision (mAP) score.
    """
    average_precision = []
    num_classes = len(set([gt['label'] for gt in ground_truths]))

    for c in range(num_classes):
        class_predictions = [pred for pred in predictions if pred['label'] == c]
        class_ground_truths = [gt for gt in ground_truths if gt['label'] == c]

        precisions = []
        recalls = []

        for threshold in np.arange(0.5, 1.0, 0.05):  # Vary IoU threshold from 0.5 to 0.95
            precisions_at_threshold = []
            recalls_at_threshold = []

            for prob_thresh in np.arange(0.0, 1.05, 0.05):  # Vary confidence threshold from 0 to 1
                precision, recall = calculate_precision_recall(class_predictions, class_ground_truths,
                                                               prob_threshold=prob_thresh,
                                                               overlap_threshold=threshold)
                precisions_at_threshold.append(precision)
                recalls_at_threshold.append(recall)

            avg_precision = np.mean(precisions_at_threshold)
            precisions.append(avg_precision)
            recalls.append(np.mean(recalls_at_threshold))

        average_precision.append(np.mean(precisions))

    mAP = np.mean(average_precision)

    return mAP


# Example data
predictions = [
    {'label': 0, 'probability': 0.9, 'bounding_box': [100, 100, 50, 50]},  # label 0, high confidence
    {'label': 1, 'probability': 0.8, 'bounding_box': [200, 200, 50, 50]},  # label 1, high confidence
    {'label': 0, 'probability': 0.7, 'bounding_box': [120, 120, 40, 40]},  # label 0, medium confidence
    {'label': 1, 'probability': 0.6, 'bounding_box': [210, 210, 60, 60]},  # label 1, medium confidence
]

ground_truths = [
    {'label': 0, 'bounding_box': [105, 105, 60, 60]},  # label 0
    {'label': 1, 'bounding_box': [200, 200, 50, 50]},  # label 1
]

# Calculate Precision and Recall
precision, recall = calculate_precision_recall(predictions, ground_truths, prob_threshold=0.5, overlap_threshold=0.3)
print(f'Precision: {precision:.2f}, Recall: {recall:.2f}')

# Calculate mAP
mAP = calculate_map(predictions, ground_truths, prob_threshold=0.5, overlap_threshold=0.3)
print(f'mAP: {mAP:.2f}')