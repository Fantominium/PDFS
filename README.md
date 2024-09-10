# This application requires Docker to be installed

Install from <https://docs.docker.com/engine/install/> and follow the instructions for your system
Once you do, proceed

## Building the app

### Install & Run

- When you're ready, start your application by navigating into the root of this project and run in terminal:
`docker compose up --build -d`
This runs docker compose command in detached mode, so the terminal is not occupied.

This will pull the necessary images, the python instance, into docker and run the containers.
Check Docker either via desktop or command, for a running container, named "PrequinBE"  representing the api.

Once the containers are runnning, you can navigate to the api documentation by going to <http://localhost:8181/docs> and the FastApi interface should appear, listing all the api methods that are currently accesible
