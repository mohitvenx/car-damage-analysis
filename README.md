# Car-Damage-Analysis

**SUMMER INTERNSHIP FROM JUNE-AUGUST 2022 AT iNUBE SOFTWARE SOLUTIONS PRIVATE LIMITED**

In this Project, I have created 5 models for the first 5 stages of the pipeline. 

![image](https://user-images.githubusercontent.com/79797947/181877790-ecef2998-d5bb-4d43-884c-45b8b6b11977.png)

1. The first model is a pretrained model that uses vgg16 imagenet weights to predict if the image entered is a car or not. If the image is a car, the image moves to the next stage in the pipeline else 
2. The second model is trained to check if the car is damaged or not. 
3. The third model is trained to check the damaged area ie front, Side or Rear end damage.
4. The fourth model is trained to check the severity of the damage ie minor, moderate, severe damage.
5. The fifth model is trained to draw bounding boxes around the damaged area.  
The first 2 models act as Gate Checks as only if the first 2 results are true then the image goes to the third model else the user must input another image. 
The dataset we have been provided has been annotated using Roboflow, a tool that helps us draw bouding boxes around the required area and this is then fed to the model we create which can then predict damage or scratch and draw bounding boxes around the same. 

**About**

I have trained a Faster R-CNN neural network. Faster R-CNN is a two-stage detector: first it identifies regions of interest, and then passes these regions to a convolutional neural network. The outputted features maps are passed to a support vector machine (SVM) for classification. Regression between predicted bounding boxes and ground truth bounding boxes are computed.

**Our data**

The data we are using for this project is a damaged cars dataset where we will be detecting the damage present on vehicles which are put for insurance claims.We split our dataset creating two datasets in Roboflow: train and test. We use Roboflow to generate TFRecords for each and train our own custom dataset.

**Training**

Google Colab provides free GPU resources. Click "Runtime" → "Change runtime type" → Hardware Accelerator dropdown to "GPU" and save this to default.

Colab does have memory limitations, and notebooks must be open in your browser to run. Sessions automatically clear themselves after 12 hours.


**Post testing**
1. After testing the model with our images if results are satisfying we can go to the next step in which we use the weights we downloaded onto gdrive or laptop and write a function with these weights being called to predict bbox ariound the damaged area.(this is toi achieve quick outputs and saves us the trouble of re-running the entire model everytime) 
2. If we are unhappy with the results being shown, we add more images onto roboflow and annotate them and repeat the entire process till we achieve required mAP and prediction percentage. 
