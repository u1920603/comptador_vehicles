 #!/bin/bash

xhost +local:
docker-compose -f infrastructure.yml up --build

