#!/bin/sh
#FROM alpine:latest
FROM python:3.9


RUN pip install pip pip --upgrade

#RUN python3 -m pip install requests
ENV PYTHONUNBUFFERED 1
#WORKDIR /damaged_cars

#COPY . /damaged_cars
RUN mkdir /damaged_cars
WORKDIR /damaged_cars
COPY requirements.txt /damaged_cars/

COPY area-bbox-test /damaged_cars/
COPY file_input /damaged_cars/
COPY h5_files /damaged_cars/
COPY pb_files /damaged_cars/
COPY object_detection /damaged_cars/
#ADD object_detection /damaged_cars/
COPY pb_files/ /damaged_cars/
COPY app.py /damaged_cars/
COPY damagearea_bbox.py /damaged_cars/
COPY product.py /damaged_cars/
#COPY ./object_detection/utils/label_map_util.py damaged_cars/object_detection/utils/
COPY object_detection/ damaged_cars/object_detection/


#RUN pip install object-detection
RUN pip install -r requirements.txt
#RUN pip install tensorflow-object-detection-api

RUN apt-get update && apt-get install -y python3-opencv


#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0

#CMD python app.py

EXPOSE 5000

#ENTRYPOINT [ "python3" ]

#CMD [ "./app.py"]
#CMD [ "app.py" ]
CMD python app.py
