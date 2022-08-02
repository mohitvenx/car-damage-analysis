# Car-Damage-Analysis

   *SUMMER INTERNSHIP FROM JUNE-AUGUST 2022 AT iNUBE SOFTWARE SOLUTIONS PRIVATE LIMITED*

![image](https://user-images.githubusercontent.com/79797947/181878018-a0c08a00-2bf4-4a14-af80-520cba50f208.png)   

This product has been developed for iNUBE, an Insurance industry software development and services company based in Bangalore, Karnataka. iNube also processes insurance claims for its clients (Insurance companies in India and the rest of the world) and therefore, sees a lot of potential in automating the process of settlement of accident damage insurance claims for vehicles. 

This product is an example of the application of Deep Learning and Computer Vision into automating the damage assessments, by building and training Convolution Neural Networks. Motor Claims passes through multiple checks that ensure that 

•	The given image is that of a car and 

•	then ensure that it is in fact damaged. 

These are the gate checks before the analysis begins. Once these gate checks have been validated, the damage check will commence. The AI / ML model will then predict the location of the damage as in the front, side or rear of the vehicle and the severity of such a damage as in minor, moderate or severe damage. 

The objective of building this product is 

•	to detect damages from minor scratches to severe damage in vehicles using images taken at the scene of the accident. 

•	to detect and label the various areas and parts damaged in the image entered. This is displayed as an image with bounding boxes around the damaged area and parts and texts labelling the damaged parts. The cost estimate for the damaged parts is then provided. 

The following model used has been shown as a pipeline in the image shown below.
![image](https://user-images.githubusercontent.com/79797947/181877790-ecef2998-d5bb-4d43-884c-45b8b6b11977.png)

1. The first model is a pretrained model that uses vgg16 imagenet weights to predict if the image entered is a car or not. If the image is a car, the image moves to the next stage in the pipeline else 
2. The second model is trained to check if the car is damaged or not. 
3. The third model is trained to check the damaged area ie front, Side or Rear end damage.
4. The fourth model is trained to check the severity of the damage ie minor, moderate, severe damage.
5. The fifth model is trained to draw bounding boxes around the damaged area.  

The dataset I have used has been annotated using Roboflow, a tool that helps us draw bouding boxes around the required area and this is then fed to the model we create which can then predict damage or scratch and draw bounding boxes around the same. 



**RESULTS OF THE FINAL PRODUCT**

•	On vehicle and damage detection the model has achieved a 91% accuracy and 

•	for the location and severity of damage the model has a 84% and 85% accuracy respectively. 

•	For detecting the damage and displaying it with a bounding box, the model shows an accuracy of 95.8%. This is an encouraging mark obtained with a dataset of about 8000 images. 

![image](https://user-images.githubusercontent.com/79797947/182276507-bfbc479e-2107-4253-9102-90c57db811ac.png)


With a larger dataset for training the model, the results would be higher and place this product on accuracy levels better than trained human beings. Even though the model for predicting bounding boxes around the damaged area is highly accurate, after integration of all the models making a pipeline, the final product has an accuracy of 90%. 



**Current Restrictions in the Model**

There are a couple of restrictions for the model  

•	the image size must be below 10MB (taken in a 12 MP or 16 MP mode)  

•	for damages located at different regions the user has to input different images with each image covering one region of the car for accurate detection.

•	Incase of damage to 2 or more areas, the bounding box identifies the damage across the 2 or more areas 
