#!/bin/bash
read -p "Build Docker? (y/n): " build_docker

if [ "$build_docker" == "y" ]; then
    # BUILD DOCKER. Where: thesis/fastseg3d:0.1 = container_name
    docker build -t ids4swc/docker:0.1 -f Dockerfile.ids4swc .
fi

read -p "What Operating System are you using? Windows or Linux (W/L): " run_os
read -p "Run Docker Jupyter or Bash? (J/B): " run_docker

if [ "$run_os" == "W" ]; then
    pwd_var="C:/Program Files/Git/home/PhD_Private"
fi

if [ "$run_os" == "L" ]; then
    pwd_var=$(pwd)
fi

# to run jupyter notebook: 
# jupyter notebook --allow-root --ip 0.0.0.0 --no-browser OR
# jupyter notebook --allow-root --ip=0.0.0.0 --port=8888 --no-browser
if [ "$run_docker" == "J" ]; then
    docker run -it --rm --name ids_jupyter \
        -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes \
        --mount type=bind,source="$pwd_var",target=/src \
        ids4swc/docker:0.1 \
        bash
fi

if [ "$run_docker" == "B" ]; then
    docker run -it --rm --name ids_bash \
        --mount type=bind,source="$pwd_var",target=/src \
        ids4swc/docker:0.1 \
        bash
fi
