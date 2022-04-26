
# npr-directions
![test_workflow](https://github.com/razalamb1/npr-directions/actions/workflows/tests.yml/badge.svg)

This repo supports a web application to provide NPR radio stations along a directional driving route. The web application is live, deployed on AWS App Runner and can be found [here](https://u7xdjayug8.us-east-2.awsapprunner.com/). The application takes user input origin and destination and returns an image containing a driving route, color coded by NPR station frequencies. Please be patient with requests, as they can take up to 10 seconds. An example is included below. In this case, the user asked for directions from New York, NY to Washington, D.C.

![Alt Text](https://github.com/razalamb1/npr-directions/blob/main/images/IMG_4404.png?raw=True)

This web application talks to the [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/overview) and the [NPR Station API](https://dev.npr.org/api/?urls.primaryName=station) in order to determine NPR stations nearest to a driving direction route. A flowchart of this process can be found below.

![Alt Text](https://github.com/razalamb1/npr-directions/blob/main/images/npr.png?raw=True)

## Getting Started

## Getting Started
If you would like to run the flask app locally, run the commands below.

**Step 1: Clone the repo.**
```
git clone https://github.com/razalamb1/npr-directions.git
```

**Step 2: Navigate your way into the repo.**
```
cd npr-directions
```

**Step 3: Run the Makefile to install and/or update requirements.**
```
make install
```

**Step 4: Obtain API Keys for Google Maps and NPR.**
In order to run this, you will need to get an API key for [Google Maps](https://developers.google.com/maps/documentation/javascript/get-api-key) and [NPR](https://dev.npr.org/guide/prerequisites/). Then you will need to create a `.env` file with these API keys in the root directory **and** the `src` folder, following the format from [the provided example](getting_started/.env_example).

**Step 5: Run the flask app locally by executing main.py.**
```
python flask_app.py
```

**Authors**: (Raza Lamb)[https://github.com/razalamb1], (Peining Yang)[https://github.com/peiningyang]


