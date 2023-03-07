## This is DRF project example with:
#### 1. JWT Authentication.
- based on simple-jwt
#### 2. Users Endpoints:
- based on djoser
#### 3. News Model with comments and likes with:
- Viewsets
- GenericAPIViews
- APIViews
- annotation for ORM
#### 4. Celery:
- _/api/v1/news/{id}/send-email/_
#### 5. Documentation:
- based on drf-yasg
- _/swagger/_
- _/redoc/_
#### 6. Django Debug Toolbar and Admin Panel in debug mode.
#### 7. Filters:
- based on django-filter
- _/api/v1/news/_

## Docker

#### Build.

```sh
sudo docker-compose build
```

#### Start.

```sh
sudo docker-compose up
```

#### Restart drf-server for development.

```sh
sudo docker-compose up -d --no-deps --build server
```
#### Start in detached mode.

```sh
sudo docker-compose up --build -d
```

#### Stop.

```sh
sudo docker-compose stop
```


## Contribution

#### Thank you to [saqibur](https://github.com/saqibur/) for a [ django-project-structure](https://github.com/saqibur/django-project-structure).