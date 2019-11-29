# pyzmq-client
Steps to connect client

With Docker
1) Create docker file
    
2) Build and run docker image file

    ```docker-compose up ```
    

Without Docker Image
1) Create virtualenv

2) Install requirement.txt

    ```pip install -r requirement.txt```
    
3) Set ip of server in ENV variable
    e.g., server_url="tcp://10.0.28.221:5555"

4) Set ENV variable 

    ```export api_url=http://10.0.28.221:5000```

5) Run Flask project:

    ```python user-reg.py```

6) Now app is running at http://127.0.0.1:5001/


