# pyzmq-client
Steps to connect client

With Docker
1) Create docker file
    
2) Build docker image file

    ```docker build -t python-client .```
    
3) Run docker image file

    ```docker run --network="host" python-client```

Without Docker Image
1) Create virtualenv

2) Install requirement.txt

    ```pip install -r requirement.txt```
    
3) Set ip of server in ENV variable
    e.g., server_url="tcp://10.0.28.216:5555"
4) Set ENV variable 

    ```FLASK_APP=client.py```

5) Run Flask project:
    ```flask run```

6) Now app is running at http://127.0.0.1:5000/


