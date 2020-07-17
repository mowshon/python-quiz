# syntax=docker/dockerfile:experimental

FROM python:3.7-alpine

WORKDIR /opt/app/

COPY python_quiz/requirements.txt /opt/app/requirements.txt
RUN pip3 install -r /opt/app/requirements.txt

COPY python_quiz /opt/app

# Uncomment these lines if you want not to delete data after restarting the container
# Now the data is stored in the project folder in the container and will be deleted after the container is recreated
#VOLUME ["/path/to/database:/opt/db"]  ## Change db_path to "/opt/db" in configs/prod.yaml
#VOLUME ["/path/to/questions:/opt/questions"]  ## Change questions_path to "/opt/questions" in configs/prod.yaml
#VOLUME ["/path/to/images:/opt/images"]  ## Change images_path to "/opt/images" in configs/prod.yaml
#VOLUME ["/path/to/coding:/opt/coding"]  ## Change coding_path to "/opt/coding" in configs/prod.yaml

ENV PYTHONPATH=/opt/app:${PYTHONPATH}
ENV PATH=/opt/app:${PATH}

ENTRYPOINT ["main.py"]
