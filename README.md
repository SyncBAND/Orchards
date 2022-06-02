# Orchards
Project for farmers to view and analyze data.


# How to use

Use the link below to get a list of (potentially) missing trees in an orchard

    https://aerobotics.metsiapp.co.za/orchards/{orchard_id}/missing-trees/

given an {orchard_id} you have access to. For example
    
    https://aerobotics.metsiapp.co.za/orchards/216269/missing-trees/

For fun, you can plot your initial data set by using the link below to have a sense of where the missing trees could be

    https://aerobotics.metsiapp.co.za/orchards/216269/missing-trees/?draw

> Note: you'll have to zoom into the map to see more


# Local Setup 

## If you are using docker. 

Pull the image

    sudo docker pull tyrofest/orchards:app

Create a file on your desktop called `docker-compose.yml` and paste and save the following

    version: '3'
    services:
        app:
        container_name: app
        command: sh -c "/home/aero/app/entrypoint.sh"
        restart: unless-stopped
        volumes:
            - uwsgi_log:/var/log/uwsgi
            - static_volume:/home/aero/app/orchards/static
        image: tyrofest/orchards:app
        ports:
            - "9000:80"

    volumes:
        static_volume:
        uwsgi_log:

> you can change the ports 

Open your terminal and change directory to your desktop or where you saved the file

    docker compose up

Go to your browser and paste the url

    http://localhost:9000/


## Alternatively, create a virtual env 

> Tested using python 3.8 and Django 3.2

    git clone https://github.com/SyncBAND/Orchards.git
    cd Orchards/
    pip install -r requirements.txt
    python migrate
    python collectstatic
    python manage.py createsuperuser

You will need an API_TOKEN to make requests. To insert your token, login as the 
administrator and proceed to

    http://localhost:8000/admin/constance/config/

Paste your token, make sure the BASE_ENDPOINT is correct and save. Test with orchard ids at your disposal by replacing the variable, {orchard_id}

    http://localhost:8000/orchards/{orchard_id}/missing-trees/

> Replace the port number above if you are not using 8000


# Deploy

I use Github's workflow to deploy the app. Essentially, I build the Docker image in the pipeline to make sure there are no errors before deploying onto the prod/staging environment. If all is well, the image is updated and pushed up to Docker hub. 

The script then logs onto the server, does some cleaninng up before pulling the latest image from a different `docker-compose.yml` file (contents of the file can be seen above) and runs the app.


# Things to take note of

## Assumptions

The workflow script assumes the server/cloud environment is setup already. That to say, docker is installed and the web server is configured. We can automate the process by using a configuration management tool which is left for you to do :) (I like using Ansible)

