
# npr-directions
![test_workflow](https://github.com/razalamb1/npr-directions/actions/workflows/tests.yml/badge.svg)

This repo supports a web application to provide NPR radio stations along a directional driving route. The web application is live, and can be found [here](https://u7xdjayug8.us-east-2.awsapprunner.com/). The application takes user input origin and destination and returns an image containing a driving route, color coded by NPR station frequencies. Please be patient with requests, as they can take up to 10 seconds. An example is included below. In this case, the user asked for directions from New York, NY to Washington, D.C.

![Alt Text](https://github.com/razalamb1/npr-directions/blob/main/images/IMG_4404.png?raw=True)

This web application talks to the [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/overview) and the [NPR Station API](https://dev.npr.org/api/?urls.primaryName=station) in order to determine NPR stations nearest to a driving direction route. The user provides a starting and ending address, and the application returns a set of NPR stations and their frequency.


![Alt Text](https://github.com/razalamb1/npr-directions/blob/main/images/npr.png?raw=True)
