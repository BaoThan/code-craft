docker pull ubuntu &&\
    docker build -t code-craft . &&\
    docker run -p 5000:5000 --name code-craft code-craft
