#!/bin/bash


# api
docker rm $POPZIM_API_CONTAINER_NAME

docker rmi $POPZIM_API_IMAGE_NAME

docker build -f $POPZIM_API_CONFIG_DIR/$POPZIM_API_DOCKERFILE -t $POPZIM_API_IMAGE_NAME $POPZIM_API_CONFIG_DIR

docker run -d --name=$POPZIM_API_CONTAINER_NAME \
           -p $POPZIM_API_HOST_PORT:$POPZIM_API_CONTAINER_PORT \
           --mount type=bind,source=$POPZIM_BASE_DIR/$POPZIM_API_HOST_DIR,target=$POPZIM_API_CONTAINER_DIR \
           api:2

docker stop $POPZIM_API_CONTAINER_NAME


# server
docker rm $POPZIM_SERVER_CONTAINER_NAME

docker rmi $POPZIM_SERVER_IMAGE_NAME

docker build -f $POPZIM_SERVER_CONFIG_DIR/$POPZIM_SERVER_DOCKERFILE -t $POPZIM_SERVER_IMAGE_NAME $POPZIM_SERVER_CONFIG_DIR

docker run -d --name=$POPZIM_SERVER_CONTAINER_NAME \
           -p $POPZIM_SERVER_HOST_PORT:$POPZIM_SERVER_CONTAINER_PORT \
           --mount type=bind,source=$POPZIM_BASE_DIR,target=$POPZIM_SERVER_CONTAINER_DIR \
           $POPZIM_SERVER_IMAGE_NAME

docker exec $POPZIM_SERVER_CONTAINER_NAME sh -c "cp /app/config/server/nginx.conf /etc/nginx/nginx.conf; cp /app/config/server/uwsgi_params /etc/nginx/uwsgi_params"

docker stop $POPZIM_SERVER_CONTAINER_NAME
