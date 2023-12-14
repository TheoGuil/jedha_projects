# GetAround Project

## Introduction

GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide. 

As Jedha's partner, they offered this great challenges: 

### Context 

When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

* Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
* Compare fuel levels.
* Measure how many kilometers were driven.

The checkin and checkout of our rentals can be done with three distinct flows:
* **📱 Mobile** rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
* **Connect:** the driver doesn’t meet the owner and opens the car with his smartphone
* **📝 Paper** contract (negligible)

### Project 🚧

For this case study, we suggest that you put yourselves in our shoes, and run an analysis we made back in 2017 🔮 🪄

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

### Goals 🎯

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

**Our Product Manager still needs to decide:**
* **threshold:** how long should the minimum delay be?
* **scope:** should we enable the feature for all cars?, only Connect cars?

In order to help them make the right decision, they are asking you for some data insights. Here are the first analyses they could think of, to kickstart the discussion. Don’t hesitate to perform additional analysis that you find relevant.

* Which share of our owner’s revenue would potentially be affected by the feature?
* How many rentals would be affected by the feature depending on the threshold and scope we choose?
* How often are drivers late for the next check-in? How does it impact the next driver?
* How many problematic cases will it solve depending on the chosen threshold and scope?

#### Web dashboard

First build a dashboard that will help the product Management team with the above questions. You can use `streamlit` or any other technology that you see fit. 


#### Machine Learning - `/predict` endpoint

In addition to the above question, the Data Science team is working on *pricing optimization*. They have gathered some data to suggest optimum prices for car owners using Machine Learning. 

You should provide at least **one endpoint** `/predict`. The full URL would look like something like this: `https://your-url.com/predict`.

This endpoint accepts **POST method** with JSON input data and it should return the predictions. We assume **inputs will be always well formatted**. It means you do not have to manage errors. We leave the error handling as a bonus.

## Guide

Pour démarrer le projet en dev, il faut téléchargé l'extension `devcontainer` de VS Code.

Une fois installé, il faut `Rebuild and Reopen in container` le container une première fois via les commandes de l'extension. Ensuite il suffira de le `reopen`.

### Dashboarding

URL : https://theo-jedha-deploy-dash-486bb96ea964.herokuapp.com/

Une fois le container construit, pour démarrer le server streamlit, il faut executer les commandes :

``` shell
cd dashboard/
```
puis 
``` shell
streamlit run --server.port 80 ./home.py
```

le dashboard sera disponible au port défini dans le fichier .devcontainer/devcontainer.json

### API

URL : https://theo-jedha-deploy-api-60d18a35346f.herokuapp.com/documentation

Pour démarrer le server FastAPI, il faut executer les commandes :

``` shell
cd api/
```
puis 

en dev pour avoir l'auto-reload
``` shell
uvicorn app:app --port 80 --host 0.0.0.0 --reload
```

sinon
``` shell
gunicorn app:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
```

