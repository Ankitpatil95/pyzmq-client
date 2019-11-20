# pyzmq-client
Steps to connect client

With Docker
1)Set ip of server in ENV variable
    e.g., server_url="tcp://10.0.28.221:5555"
    
2) Build docker image file

    ```docker build -t python-client .```
    
3) Run docker image file

    ```docker run -a stdin -a stdout -i -t --network="host" python-client```

Without Docker Image
1) Create virtualenv

2) Install requirement.txt

    ```pip install -r requirement.txt```
    
3) Set ip of server in ENV variable
    e.g., server_url="tcp://10.0.28.221:5555"
4) Run Client File

    ```python client.py```
