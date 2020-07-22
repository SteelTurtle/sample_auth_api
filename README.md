## Sample Auth Api (Or: a totally unfinished Django 3 based skeleton project for an API)
### ...with multi-factor authentication, which is better than nothing!

This API was born as a prototype for a commercial service that ended up being done, well, in a very 
different way. Rather than throwing the unused prototype, I thought it was useful to make the prototype public, 
mainly to show how easy and quick is to build Rest API with Python and Django 3
(courtesy of the excellent [**Django REST Framework**]), completed with 2-Factor-Authentication
 capabilities offered by the [**django_trench**] library.
 The API is also configured to use [**django_channels**] for eventual implementation of real time 
 messaging. No functionality is provided in this sense though. (You know, it was out of scope for the prototype :D) 

### How to launch and use the API
I assume you are already a Python developer with relevant experience using the Django framework.
I also assume you know how to use Docker and docker-compose to spawn reusable 
containers on your local machine.
To see the auth service in action, just launch the environment with docker-compose form the root directory of the 
cloned repository:

    docker-compose up -d --build

The api listen for all request on: `http://0.0.0.0:8000`, and the
relevant endpoints to initiate the authentication workflow are reachable through the path `api/v1/user/**`.
Overall, this basic authorization service is a good starting point to build consumable APIs of any
kind, excluding of course cases where you need way more power than a 
traditional "username->password->token" approach. In that case, you are probably looking 
for **_Oauth2_**!

[**Django REST Framework**]: https://www.django-rest-framework.org/
[**django_trench**]: https://github.com/merixstudio/django-trench
[**django_channels**]: https://channels.readthedocs.io/en/latest/
