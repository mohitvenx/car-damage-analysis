FROM python:3.9

RUN pip install pip pip --upgrade
ENV PYTHONUNBUFFERED 1
VOLUME ./:app/

COPY . /app/



# Change WORKDIR
WORKDIR /app

# Install dependencies
# use --proxy http://<proxy host>:port if you have proxy
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
# In Docker, the containers themselves can have applications running on ports. To access these applications, we need to expose the containers internal port and bind the exposed port to a specified port on the host.
# Expose port and run the application when the container is started
EXPOSE 9999:9999
ENTRYPOINT python app.py 9999
CMD ["app.py"]
