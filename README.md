# Crack Detection Project

The purpose of this project is to compare the performances of 3 approaches (Azure Custom Vision, Faster R-CNN, and YOLO) on the given two datasets (SeamTaping and WRB).

## Preparation

### Prepare Python environment on local machine for this project.

Install **Miniconda**.

Then, launch **Anaconda Prompt (miniconda3)**.

```Anaconda
(base) C:\Users\User>D:
(base) D:\>cd Work
(base) D:\Work>conda create -n Crack-Detection python
(base) D:\Work>conda activate Crack-Detection
(Crack-Detection) D:\Work>pip install scikit-learn pandas openpyxl matplotlib pillow tqdm requests azure-cognitiveservices-vision-customvision python-dotenv
```

### Create an AI Services - Custom Vision resource on Azure and get the keys, ids, and endpoints.

Create an AI Services - Custom Vision resource on Azure starting from here: [Home - Microsoft Azure](https://portal.azure.com/#home)

Get the keys, ids, and endpoints: [Custom Vision - Settings](https://www.customvision.ai/projects#/settings)


## Check and Update the Two Datasets

There are 2 original datasets given in XLSX files:

- [WRB Bad Detection](dataset/WRB_All.xlsx)
- [SeamTaping Damaged Detection](dataset/SeamTaping_All.xlsx)

Please run the 5 notebooks in the subfolder '/dataset_check_update' before trying 3 approaches.

## Try Three Approaches

- Azure Custom Vision

    In Azure Custom Vision, we don't get the option to explicitly select the underlying object detection model type such as Faster R-CNN, YOLO, or SSD. Azure Custom Vision abstracts away these implementation details to provide a simplified and user-friendly interface for training and deploying custom object detection models.
    While Azure Custom Vision simplifies the process of training and deploying object detection models, it does not provide the flexibility to choose specific underlying algorithms like Faster R-CNN or YOLO.

    * Dataset injection to Azure Custom Vision
        + [SeamTaping Dataset Injection](<different-approaches/azure-custom-vision/1. SeamTaping_dataset-inject.ipynb>)
        + [WRB Dataset Injection](<different-approaches/azure-custom-vision/1. WRB_dataset-inject.ipynb>)

    * Train Model
        + [SeamTaping Model Training](<different-approaches/azure-custom-vision/2. SeamTaping_train-model.ipynb>)
        + [WRB Model Training](<different-approaches/azure-custom-vision/2. WRB_train-model.ipynb>)

    * Evaluate Performance
        + [SeamTaping Model Evaluation](<different-approaches/azure-custom-vision/3. WRB_evaluate-model.ipynb>)
        + [WRB Model Evaluation](<different-approaches/azure-custom-vision/3. WRB_evaluate-model.ipynb>)

- Fasteer R-CNN

- YOLO v10
