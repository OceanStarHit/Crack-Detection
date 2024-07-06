# GPT Prompts

## Azure Custom Vision

In Azure Custom Vision Object Detection project, there are 2 thresholds (Probability Threshold and Overlap Threshold) and 3 metrics (Precision, Recall, and mAP) for trained model performance.

Please write a code to calculate the metrics.

In Azure Custom Vision Object Detection project, there are 2 thresholds (Probability Threshold and Overlap Threshold) and 3 metrics (Precision, Recall, and mAP) for trained model performance.

I have a object detection dataset where there are image URLs.

The dataset format is:

[
    {
        "image_file_name": "997126.jpg",
        "image_urls": [
            "https://example.com/997126.jpg",
            "https://example.com/997126.jpg",
            "https://example.com/997126.jpg"
        ],
        "annotations": [
            {
                "label": "WRB-Bad",
                "bbox": [315.63, 403.59, 68.88, 56.53]
            },
            {
                "label": "WRB-Bad",
                "bbox": [420.25, 392.22, 49.38, 32.49]
            }
        ]
    },

    ...
]

bbox format: x_min, y_min, width, height

I have trained a custom vision model and published the iteration.

project.id and publish_iteration_name

Please write a clean code using separated function to evaluate the trained model, that is,  Precision, Recall, and mAP based on Probability Threshold and Overlap Threshold.

## Faster R-CNN

I'd like to optimize hyper parameters of torchvision FasterRCNN(Resnet50) using Optuna.

Model: TorchVision FasterRCNN with ResNet50
Image size: 800*800
Num of classes: 1

Specify the range or possible values for each hyperparameter.

- Learning Rate: [0.001, 0.01]
- Batch Size: [8, 16, 32]
- Number of Epochs: [10, 20, 30]
- Optimizer: [SGD, Adam]
- Anchor Sizes and Ratios: Experiment with different combinations.

evaluation metric: validation loss

Please write the complete code
